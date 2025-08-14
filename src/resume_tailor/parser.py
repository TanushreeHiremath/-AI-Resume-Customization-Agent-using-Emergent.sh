# src/resume_tailor/parser.py
import re
from pdfminer.high_level import extract_text
from io import BytesIO

def extract_text_from_pdf(path):
    """
    Extract text from a PDF file at 'path' using pdfminer.six
    """
    return extract_text(path)

def extract_text_from_pdf_bytes(pdf_bytes):
    """
    Extract text from PDF bytes (useful for file uploads)
    """
    fp = BytesIO(pdf_bytes)
    return extract_text(fp)

def normalize(text):
    if not text:
        return ""
    text = text.replace("\r", "\n")
    # collapse multiple spaces
    text = re.sub(r"[ \t]+", " ", text)
    # collapse many blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()

def split_lines(text):
    return [ln.strip() for ln in text.splitlines() if ln.strip()]

def probable_sections(lines):
    """
    crude header recognition: returns dict with sections like summary, experience, skills, education
    """
    sections = {}
    current = "body"
    buffer = []
    for ln in lines:
        low = ln.lower().strip(": ")
        if low in ("summary", "objective", "experience", "work experience", "projects", "skills", "education", "certifications"):
            if buffer:
                sections.setdefault(current, []).append("\n".join(buffer).strip())
                buffer = []
            current = low.replace("work experience", "experience")
            continue
        buffer.append(ln)
    if buffer:
        sections.setdefault(current, []).append("\n".join(buffer).strip())
    # join multi parts
    for k, v in list(sections.items()):
        sections[k] = "\n\n".join(v).strip()
    return sections

def bullets_from_text(text):
    """
    Find bullets in a block of text (bulleted lists or sentences).
    """
    if not text:
        return []
    # split on common bullet markers as well as newline sentences
    raw = re.split(r"(?:^|\n)\s*(?:[-*•]\s+)", "\n" + text)
    outs = []
    for ch in raw:
        s = ch.strip()
        if not s:
            continue
        parts = re.split(r"(?<=[.;])\s+", s)
        for p in parts:
            p = p.strip()
            if p and len(p.split()) >= 3:
                outs.append(p)
    # fallback: try sentences by newline if none found
    if not outs:
        for ln in text.splitlines():
            ln = ln.strip()
            if len(ln.split()) >= 4:
                outs.append(ln)
    return outs
