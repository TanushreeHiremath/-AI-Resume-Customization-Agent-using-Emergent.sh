# src/resume_tailor/rewriter.py
import re
from resume_tailor.matcher import extract_tokens

ACTION_VERBS = [
    "Led","Owned","Built","Developed","Designed","Implemented","Optimized","Automated",
    "Deployed","Launched","Migrated","Refactored","Analyzed","Improved","Reduced","Increased",
    "Drove","Created","Standardized","Streamlined","Orchestrated","Coordinated","Supported","Assisted"
]

BULLET = "•"

def score_bullet(b, jd_kw):
    toks = set(extract_tokens(b))
    hits = toks.intersection(set([w.lower() for w in jd_kw]))
    has_num = 1 if re.search(r"\b\d+(\.\d+)?%?\b", b) else 0
    return len(hits) * 2 + has_num

def smart_rewrite(b, jd_kw):
    b2 = b.strip()
    # ensure it starts with an action verb (if not, prepend a conservative verb)
    if not any(b2.startswith(v) for v in ACTION_VERBS):
        # avoid fabricating — keep original text but prepend generic verb
        b2 = f"Supported {b2[0].lower() + b2[1:]}" if b2 else b2
        # capitalize first word
        b2 = b2[0].upper() + b2[1:]
    # minimal cleanup: collapse internal whitespace
    b2 = re.sub(r'\s+', ' ', b2)
    return b2

def order_and_rewrite_bullets(bullets, jd_kw, max_n=10):
    scored = [(score_bullet(b, jd_kw), b) for b in bullets]
    scored.sort(key=lambda x: (-x[0], -len(x[1])))
    picked = []
    seen = set()
    for s, b in scored:
        key = b.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        picked.append(smart_rewrite(b, jd_kw))
        if len(picked) >= max_n:
            break
    return picked

def assemble_resume(target_title, summary_text, skills, selected_bullets, extra_sections_text=None):
    lines = []
    lines.append(f"{target_title.upper()} — CUSTOMIZED RESUME")
    lines.append("")
    lines.append("SUMMARY")
    lines.append(summary_text.strip() if summary_text else f"{target_title} with relevant experience and strengths in {', '.join(skills[:6])}.")
    lines.append("")
    lines.append("CORE SKILLS")
    lines.append(", ".join(skills) if skills else "—")
    lines.append("")
    lines.append("EXPERIENCE (SELECTED & REORDERED)")
    if selected_bullets:
        for b in selected_bullets:
            lines.append(f"{BULLET} {b}")
    else:
        lines.append("—")
    lines.append("")
    if extra_sections_text:
        lines.append("ADDITIONAL")
        lines.append(extra_sections_text)
    return "\n".join(lines)
