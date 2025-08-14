# src/resume_tailor/matcher.py
import re
from collections import Counter

STOPWORDS = set("""
a an the and or of to in for with on at from by into through during including until while
is are was were be been being as that which who whom this these those
""".split())

# add healthcare & consulting relevant skills and common tech
SKILL_LEXICON = {
    "python","excel","sql","tableau","powerbi","redcap","spreadsheets","r","spss","pandas","numpy",
    "data analysis","clinical","clinical trials","regulatory","gcp","patient","research","healthcare",
    "payment models","strategy","project management","stakeholder","qualitative","quantitative",
    "interviews","presentations","ppt","powerpoint","communication","writing","reporting","analytics"
}

def extract_tokens(text):
    text = (text or "").lower()
    tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9\+\-\.#]{1,}", text)
    return [t for t in tokens if t not in STOPWORDS and len(t) > 1]

def extract_skills(text):
    toks = set(extract_tokens(text))
    hits = set()
    for s in SKILL_LEXICON:
        if s.lower() in text.lower():
            hits.add(s)
    # also include capitalized tech tokens like "REDCap" or "GCP"
    caps = set(re.findall(r"\b([A-Z][A-Za-z0-9\+\-\.#]{2,})\b", text))
    caps = {c for c in caps if c.lower() not in STOPWORDS}
    for c in caps:
        hits.add(c)
    return sorted(hits)

def jd_requirements(jd_text):
    jd = jd_text or ""
    # simple heuristics: look for "Requirements", "Desired Skills", "Responsibilities"
    keywords = extract_skills(jd)
    freq = Counter(extract_tokens(jd))
    common = [w for w, c in freq.most_common(60) if c >= 2 and len(w) > 2]
    # include nouns that appear frequently
    keywords = list(dict.fromkeys(keywords + common))
    return keywords

def detect_title(jd_text):
    if not jd_text:
        return "Target Role"
    # look for first line with "Associate", "Consultant", etc.
    m = re.search(r'(?i)\b(title|role)\s*:\s*([^\n,]+)', jd_text)
    if m:
        return m.group(2).strip()
    # fallback: look for first capitalized phrase
    m2 = re.search(r'\b([A-Z][a-z]+(?:\s[A-Z][a-z]+){0,3})\b', jd_text)
    if m2:
        return m2.group(1).strip()
    return "Target Role"
