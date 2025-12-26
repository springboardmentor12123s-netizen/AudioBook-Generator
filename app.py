"""
AudioBook Generator - Flask Application
Simple web app to convert documents to audiobooks
"""

import os
import uuid
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename

from config import (
    GEMINI_API_KEY,
    ELEVENLABS_API_KEY,
    UPLOAD_FOLDER,
    OUTPUT_FOLDER,
    MAX_CONTENT_LENGTH,
    allowed_file,
    get_file_extension,
)
from modules.extractor import extract_text
from modules.enricher import enrich_text, enrich_text_simple, get_available_languages
from modules.synthesizer import text_to_speech, get_available_voices


# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def index():
    """Home page - file upload form"""
    voices = get_available_voices()
    languages = get_available_languages()
    return render_template("index.html", voices=voices, languages=languages)


@app.route("/upload", methods=["POST"])
def upload():
    """Handle file upload and process to audiobook"""

    # Check if file was uploaded
    if "file" not in request.files:
        flash("No file selected", "error")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("No file selected", "error")
        return redirect(url_for("index"))

    if not allowed_file(file.filename):
        flash("Invalid file type. Please upload PDF, DOCX, or TXT", "error")
        return redirect(url_for("index"))

    # Get voice and language selection
    voice_id = request.form.get("voice", "EXAVITQu4vr4xnSDxMaL")
    language_code = request.form.get("language", "en")
    languages = get_available_languages()
    language_name = languages.get(language_code, "English")

    # Generate unique ID for this conversion
    unique_id = str(uuid.uuid4())[:8]

    # Save uploaded file
    filename = secure_filename(file.filename)
    file_ext = get_file_extension(filename)
    upload_path = os.path.join(UPLOAD_FOLDER, f"{unique_id}_{filename}")
    file.save(upload_path)

    try:
        # Step 1: Extract text
        extract_result = extract_text(upload_path, file_ext)
        if not extract_result["success"]:
            flash(f"Text extraction failed: {extract_result['error']}", "error")
            cleanup_file(upload_path)
            return redirect(url_for("index"))

        raw_text = extract_result["text"]

        # Step 2: Enrich text with LLM (or simple cleanup if no API key)
        if GEMINI_API_KEY:
            enrich_result = enrich_text(raw_text, GEMINI_API_KEY, language_name)
        else:
            enrich_result = enrich_text_simple(raw_text)

        if not enrich_result["success"]:
            flash(f"Text enhancement failed: {enrich_result['error']}", "error")
            cleanup_file(upload_path)
            return redirect(url_for("index"))

        enhanced_text = enrich_result["text"]

        # Step 3: Convert to speech using ElevenLabs
        output_filename = f"{unique_id}_audiobook.mp3"
        output_path = os.path.join(OUTPUT_FOLDER, output_filename)

        tts_result = text_to_speech(enhanced_text, output_path, ELEVENLABS_API_KEY, voice_id)
        if not tts_result["success"]:
            flash(f"Audio generation failed: {tts_result['error']}", "error")
            cleanup_file(upload_path)
            return redirect(url_for("index"))

        # Cleanup uploaded file
        cleanup_file(upload_path)

        # Redirect to result page
        return redirect(url_for("result", filename=output_filename))

    except Exception as e:
        flash(f"An error occurred: {str(e)}", "error")
        cleanup_file(upload_path)
        return redirect(url_for("index"))


@app.route("/result/<filename>")
def result(filename):
    """Show result page with audio player and download"""
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    if not os.path.exists(output_path):
        flash("Audio file not found", "error")
        return redirect(url_for("index"))

    return render_template("result.html", filename=filename)


@app.route("/download/<filename>")
def download(filename):
    """Download the generated audio file"""
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    if not os.path.exists(output_path):
        flash("Audio file not found", "error")
        return redirect(url_for("index"))

    return send_file(
        output_path,
        as_attachment=True,
        download_name=filename,
        mimetype="audio/mpeg"
    )


@app.route("/audio/<filename>")
def serve_audio(filename):
    """Serve audio file for the player"""
    output_path = os.path.join(OUTPUT_FOLDER, filename)

    if not os.path.exists(output_path):
        return "File not found", 404

    return send_file(output_path, mimetype="audio/mpeg")


def cleanup_file(filepath):
    """Remove a file if it exists"""
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
    except Exception:
        pass


if __name__ == "__main__":
    app.run(debug=True, port=5000)
