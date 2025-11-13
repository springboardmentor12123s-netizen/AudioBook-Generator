import os
try:
    import google.generativeai as genai
    print("genai imported, version attribute:", getattr(genai, "__version__", None))
    names = sorted([n for n in dir(genai) if not n.startswith("_")])
    print("Top-level names:", names)
    print("Has chat:", hasattr(genai, "chat"))
    print("Has models:", hasattr(genai, "models"))
    print("Has GenerativeModel:", hasattr(genai, "GenerativeModel"))
except Exception as e:
    print("Import failed:", e)
