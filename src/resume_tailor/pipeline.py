# src/resume_tailor/pipeline.py
from .parser import extract_text_from_pdf, extract_text_from_pdf_bytes, normalize, probable_sections, bullets_from_text
from .matcher import jd_requirements, extract_skills, detect_title
from .rewriter import order_and_rewrite_bullets, assemble_resume
import os

def generate_custom_resume_from_files(resume_path, jd_path, use_llm=False, emergent_config=None):
    # decide text extraction based on extension
    if resume_path.lower().endswith(".pdf"):
        resume_text = extract_text_from_pdf(resume_path)
    else:
        with open(resume_path, "r", encoding="utf-8") as f:
            resume_text = f.read()

    if jd_path.lower().endswith(".pdf"):
        jd_text = extract_text_from_pdf(jd_path)
    else:
        with open(jd_path, "r", encoding="utf-8") as f:
            jd_text = f.read()

    return generate_custom_resume_from_text(resume_text, jd_text, use_llm=use_llm, emergent_config=emergent_config)

def generate_custom_resume_from_text(resume_text, jd_text, use_llm=False, emergent_config=None):
    resume_text = normalize(resume_text)
    jd_text = normalize(jd_text)

    # Parse resume sections
    sections = probable_sections(resume_text.splitlines())
    # prefer explicit parts
    exp_text = sections.get("experience") or sections.get("body") or ""
    skills_text = sections.get("skills") or ""
    summary_text = sections.get("summary") or ""

    # Extract JD keywords
    jd_kw = jd_requirements(jd_text)

    # Extract candidate skills
    resume_skills = extract_skills(resume_text)

    # Extract bullets
    bullets = bullets_from_text(exp_text)

    # pick and rewrite bullets
    selected = order_and_rewrite_bullets(bullets, jd_kw, max_n=10)

    # prioritize skills: JD-matching skills first
    prioritized = [s for s in resume_skills if any(k.lower() in s.lower() for k in jd_kw)] + [s for s in resume_skills if s not in resume_skills]
    # dedupe but preserve order
    seen = set()
    skills_list = []
    for s in prioritized:
        sl = s.lower()
        if sl not in seen:
            seen.add(sl)
            skills_list.append(s)
    skills_list = skills_list[:24]

    target_title = detect_title(jd_text) or "Target Role"

    extra = ""  # could append education/certs from sections if desired

    draft = assemble_resume(target_title, summary_text, skills_list, selected, extra_sections_text=extra)

    # Optional LLM polish
    if use_llm:
        try:
            if not emergent_config:
                emergent_config = {
                    "api_url": os.environ.get("EMERGENT_API_URL"),
                    "api_key": os.environ.get("EMERGENT_API_KEY"),
                    "model": os.environ.get("EMERGENT_MODEL", None)
                }
            from .emergent_adapter import polish_with_emergent
            polished = polish_with_emergent(draft, api_url=emergent_config.get("api_url"),
                                            api_key=emergent_config.get("api_key"),
                                            model=emergent_config.get("model"))
            return polished or draft
        except Exception as e:
            # fail gracefully and return draft
            return draft + f"\n\n[LLM polish failed: {e}]"
    else:
        return draft
