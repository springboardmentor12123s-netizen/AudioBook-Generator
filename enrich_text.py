import requests


def enrich_text(text):
    prompt = f"Rewrite the following text in an engaging, listener-friendly audiobook narration style:\n\n{text}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",   # the model you downloaded
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data["response"]