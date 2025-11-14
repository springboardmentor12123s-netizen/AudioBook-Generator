from gtts import gTTS

def create_audio(text, filename="audiobook.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename