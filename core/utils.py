import re

# Split long text into chunks for TTS processing
def split_text_for_tts(text, max_length=2500):
    text = re.sub(r"\s+", " ", text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    chunk = ""

    for sentence in sentences:
        if len(chunk) + len(sentence) <= max_length:
            chunk += " " + sentence
        else:
            chunks.append(chunk.strip())
            chunk = sentence

    if chunk:
        chunks.append(chunk.strip())

    return chunks

# Generate safe filenames for audio output
def safe_filename(name):
    return re.sub(r"[^a-zA-Z0-9_.-]", "-", name)
