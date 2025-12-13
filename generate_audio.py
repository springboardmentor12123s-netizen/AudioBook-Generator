from gtts import gTTS
from googletrans import Translator

def create_audio(text, filename="audiobook.mp3", language="en"):
    """
    Convert text to speech in different languages.
    Automatically translates text before generating audio.
    """

    translator = Translator()

    # Translate the text to the selected language
    translated = translator.translate(text, dest=language).text

    # Generate audio in selected language
    tts = gTTS(text=translated, lang=language)
    tts.save(filename)

    return filename
