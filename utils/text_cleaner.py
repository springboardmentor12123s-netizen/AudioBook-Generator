"""
text_cleaner.py
---------------------------------------------
This file cleans noisy text before:
- Converting it into speech
- Displaying extracted lyrics
- Showing PDF-extracted text

Cleaning steps:
1. Fix multiple spaces
2. Fix punctuation spacing
3. Remove weird characters
4. Remove blank lines
---------------------------------------------
"""

import re

def clean_text(text):
    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)
    text = (text.replace(" ,", ",")
                .replace(" .", ".")
                .replace(" !", "!")
                .replace(" ?", "?")
                .replace(" :", ":")
                .replace(" ;", ";"))
    text = re.sub(r"[■◆●▪◦►•]", "", text)
    text = re.sub(r"\n\s*\n", "\n", text)

    return text.strip()
