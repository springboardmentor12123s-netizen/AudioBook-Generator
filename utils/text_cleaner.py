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
    """
    Cleans and formats text to make it readable and
    suitable for audiobook generation.

    Parameters:
        text (str): Raw input text.

    Returns:
        clean_text (str): Cleaned and formatted text.
    """

    if not text:
        return ""

    # ---------------------------------------------
    # Replace multiple spaces with a single space
    # ---------------------------------------------
    text = re.sub(r"\s+", " ", text)

    # ---------------------------------------------
    # Fix punctuation spacing (e.g. "hello , world")
    # ---------------------------------------------
    text = (
        text.replace(" ,", ",")
            .replace(" .", ".")
            .replace(" !", "!")
            .replace(" ?", "?")
            .replace(" :", ":")
            .replace(" ;", ";")
    )

    # ---------------------------------------------
    # Remove unwanted symbols (common PDF issues)
    # ---------------------------------------------
    text = re.sub(r"[■◆●▪◦►•]", "", text)

    # ---------------------------------------------
    # Remove leading/trailing spaces
    # ---------------------------------------------
    text = text.strip()

    # ---------------------------------------------
    # Remove multiple newlines
    # ---------------------------------------------
    text = re.sub(r"\n\s*\n", "\n", text)

    return text
