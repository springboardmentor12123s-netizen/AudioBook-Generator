# modules/utils.py
from typing import List
from pathlib import Path
import re
import os

def chunk_text_by_chars(text: str, max_chars: int = 2000) -> List[str]:
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    chunks = []
    cur = ""
    for p in paragraphs:
        if not cur:
            cur = p
        elif len(cur) + 2 + len(p) <= max_chars:
            cur = cur + "\n\n" + p
        else:
            chunks.append(cur)
            cur = p
    if cur:
        chunks.append(cur)
    return chunks

def safe_write_text(path: str, text: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)

# Cleaning helpers
def fix_hyphenation_across_lines(text: str) -> str:
    # remove cases like "exam-\nple" -> "example"
    return re.sub(r'(?<=\w)-\s*\n\s*(?=\w)', '', text)

def remove_page_headers(text: str) -> str:
    text = re.sub(r'(?im)^\s*-{2,}\s*page\s*\d+\s*-{0,}\s*$', '', text)
    text = re.sub(r'(?im)^\s*page[:]?\s*\d+\s*$', '', text)
    return text

def normalize_whitespace_and_punctuation(text: str) -> str:
    text = re.sub(r'[_]{2,}', ' ', text)
    text = re.sub(r'[ \t]*[-–—]{2,}[ \t]*', ' ', text)
    text = re.sub(r'_', ' ', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]', '', text)
    text = re.sub(r'\r\n?', '\n', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = '\n'.join(line.strip() for line in text.splitlines())
    text = re.sub(r'([!?.,]){2,}', r'\1', text)
    text = re.sub(r'\s+([,?.!;:])', r'\1', text)
    text = re.sub(r'([.!?])(?=[A-Za-z0-9])', r'\1 ', text)
    text = re.sub(r' {2,}', ' ', text)
    return text.strip()

def make_audio_friendly(text: str) -> str:
    text = re.sub(r'\[\s*\w{1,10}\s*\]', ' ', text)
    text = re.sub(r'\(\s*\d{1,4}\s*\)', ' ', text)
    text = re.sub(r'(?m)^[\W_]+$', '', text)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def clean_extracted_text(raw: str) -> str:
    if not raw:
        return raw
    t = raw
    t = fix_hyphenation_across_lines(t)
    t = remove_page_headers(t)
    t = normalize_whitespace_and_punctuation(t)
    t = make_audio_friendly(t)
    return t
