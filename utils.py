# utils.py
import textwrap

def chunk_text(text, max_chars=15000):
    """
    Yield chunks of text not exceeding max_chars; split on sentence boundaries approximately.
    """
    text = text.strip()
    if not text:
        return []
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end]
        # expand forward to nearest newline or sentence end if possible
        if end < n:
            # try to extend to next sentence boundary
            extra_span = text[end:end+200]
            cut = None
            for sep in ['\n\n', '. ', '? ', '! ']:
                idx = extra_span.find(sep)
                if idx != -1:
                    cut = end + idx + len(sep)
                    break
            if cut:
                chunk = text[start:cut]
                start = cut
            else:
                # fallback to last space
                last_space = chunk.rfind(' ')
                if last_space > int(len(chunk)*0.6):
                    chunk = chunk[:last_space]
                    start = start + last_space
                else:
                    start = end
        else:
            start = end
        chunks.append(chunk.strip())
    return chunks