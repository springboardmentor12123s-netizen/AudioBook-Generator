import os

# Optional AI-based narration improvement
def enrich_text_with_llm(text):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return text

    try:
        import openai
        openai.api_key = api_key

        prompt = (
            "Rewrite this text in natural audiobook narration style:\n\n" + text[:4000]
        )

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1500,
            temperature=0.7
        )

        return response.choices[0].text.strip()

    except:
        return text
