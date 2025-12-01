def rewrite_for_audiobook(text: str) -> str:
    """
    Placeholder for LLM-based enrichment.
    Later replace with real OpenAI / Gemini call.
    """
    intro = (
        "This is an automatically prepared narration draft for the audiobook version "
        "of your document.\n\n"
    )
    return intro + text.strip()
