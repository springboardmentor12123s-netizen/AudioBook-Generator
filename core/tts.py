from gtts import gTTS

# Convert text to speech and save MP3 output
def text_to_speech(text, lang="en", out_path="output.mp3"):
    if not text.strip():
        text = "No readable content found."

    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(out_path)
    return out_path
