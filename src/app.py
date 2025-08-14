# src/app.py
from dotenv import load_dotenv
load_dotenv()

import os
import tempfile
from flask import Flask, request, render_template_string, send_file
from resume_tailor.pipeline import generate_custom_resume_from_text
from resume_tailor.parser import extract_text_from_pdf_bytes
from resume_tailor.pdf_exporter import generate_pdf_resume

app = Flask(__name__)

HTML = """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <title>Resume Tailor</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 900px; margin: 24px auto; padding: 0 12px; }
    textarea { width: 100%; }
    label { font-weight: bold; display:block; margin-top:12px; }
    .btn { margin-top: 12px; padding: 8px 12px; background:#1976d2; color:white; border:none; cursor:pointer; }
    .hint { color: #666; font-size: 0.9em; }
  </style>
</head>
<body>
<h1>Resume Tailor — Customize Your Resume for Any Job</h1>
<form method=post enctype=multipart/form-data>
  <label>Upload Resume PDF:</label>
  <input type=file name=resume_file accept="application/pdf"><br>
  <span class="hint">Or paste resume text in the box below.</span>
  <textarea name=resume_text rows=8 placeholder="Paste resume text (optional)"></textarea>

  <label>Upload Job Description PDF:</label>
  <input type=file name=jd_file accept="application/pdf"><br>
  <span class="hint">Or paste JD text in the box below.</span>
  <textarea name=jd_text rows=8 placeholder="Paste job description text (optional)"></textarea>

  <label><input type=checkbox name=use_llm> Use Emergent LLM polish (optional)</label><br>

  <button class="btn" type=submit>Generate Customized Resume (PDF)</button>
</form>

{% if pdf_ready %}
  <h2>Customized Resume Ready</h2>
  <a href="/download_pdf">Download PDF</a>
{% endif %}

</body>
</html>
"""

LAST_PDF_PATH = None

def _read_uploaded_pdf(file_storage):
    if not file_storage:
        return ""
    data = file_storage.read()
    return extract_text_from_pdf_bytes(data)

@app.route("/", methods=["GET", "POST"])
def index():
    global LAST_PDF_PATH
    pdf_ready = False

    if request.method == "POST":
        resume_file = request.files.get("resume_file")
        jd_file = request.files.get("jd_file")
        resume_text = request.form.get("resume_text", "").strip()
        jd_text = request.form.get("jd_text", "").strip()
        use_llm = bool(request.form.get("use_llm"))

        if resume_file and resume_file.filename:
            resume_text = _read_uploaded_pdf(resume_file)
        if jd_file and jd_file.filename:
            jd_text = _read_uploaded_pdf(jd_file)

        if not resume_text or not jd_text:
            return render_template_string(HTML, pdf_ready=False)

        customized_text = generate_custom_resume_from_text(resume_text, jd_text, use_llm=use_llm)

        # Save as PDF
        tmp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        tmp_pdf.close()
        generate_pdf_resume(customized_text, tmp_pdf.name)
        LAST_PDF_PATH = tmp_pdf.name
        pdf_ready = True

    return render_template_string(HTML, pdf_ready=pdf_ready)

@app.route("/download_pdf")
def download_pdf():
    if LAST_PDF_PATH and os.path.exists(LAST_PDF_PATH):
        return send_file(LAST_PDF_PATH, as_attachment=True, download_name="customized_resume.pdf")
    return "No PDF available. Please generate one first.", 400

if __name__ == "__main__":
    app.run(debug=True, port=5000)
