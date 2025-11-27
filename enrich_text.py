import google.generativeai as genai
genai.configure(api_key="GEMINI API KEY")

model = genai.GenerativeModel("gemini-2.5-flash")

def enrich_text(text):
    prompt = (
        "Rewrite the following text in an engaging, listener-friendly audiobook narration style.\n\n"
        f"{text}"
    )

    response = model.generate_content(prompt)

    return response.text


