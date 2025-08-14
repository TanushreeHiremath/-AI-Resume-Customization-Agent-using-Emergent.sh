# tests/test_pipeline.py
import os
from src.resume_tailor.pipeline import generate_custom_resume_from_text

def test_generate_from_text_smoke():
    resume_text = (
        "Sahil Mehta\n\nExperience\n"
        "- Conducted data analysis using SQL and Excel to support clinical trials.\n"
        "- Assisted with patient recruitment and consent.\n\nSkills\nSQL, Excel, REDCap"
    )
    jd_text = (
        "Associate Consultant, Strategy - Healthcare\n"
        "Requirements: strong analytical skills, experience with clinical research, Excel, SQL, project management."
    )
    out = generate_custom_resume_from_text(resume_text, jd_text, use_llm=False)
    assert "CORE SKILLS" in out
    assert "EXPERIENCE (SELECTED & REORDERED)" in out
