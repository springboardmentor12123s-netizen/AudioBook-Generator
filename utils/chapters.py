# utils/chapters.py

import re
from typing import List


def split_by_chapter_heading(text: str) -> List[str]:
    """
    Split text where it finds headings like:
    'Chapter 1', 'CHAPTER ONE', etc.
    If no such pattern is found, returns [text].
    """
    pattern = re.compile(r"(?:^|\n)(chapter\s+\w+\.?)", re.IGNORECASE)
    matches = list(pattern.finditer(text))

    if not matches:
        return [text.strip()] if text.strip() else []

    chapters = []
    for i, match in enumerate(matches):
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        chunk = text[start:end].strip()
        if chunk:
            chapters.append(chunk)
    return chapters


def split_into_fixed_chunks(text: str, max_chars: int = 4000) -> List[str]:
    """
    Fallback: split text into fixed-size chunks.
    """
    text = text.strip()
    if not text:
        return []

    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_chars, len(text))
        cut = text.rfind(".", start, end)
        if cut == -1 or cut <= start:
            cut = end
        chunks.append(text[start:cut].strip())
        start = cut
    return chunks


def split_into_chapters(text: str) -> List[str]:
    """
    Try chapter headings first, otherwise fixed-size chunks.
    """
    by_heading = split_by_chapter_heading(text)
    if len(by_heading) > 1:
        return by_heading
    return split_into_fixed_chunks(text)
