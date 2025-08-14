# 🚀 AI Resume Tailor

AI Resume Tailor is a Python-based application that customizes resumes for specific job descriptions using the Emergent.sh LLM API. It works both as a command-line tool and a Flask web application, helping you create ATS-friendly resumes tailored to each job application.

## ✨ Features

- **Automatic Resume Parsing** - Extracts text from PDF resumes
- **Job Description Matching** - Analyzes job requirements and maps them to resume content
- **AI-Powered Rewriting** - Uses Emergent.sh's API to rewrite your resume for better JD fit
- **ATS Optimization** - Ensures keyword-rich, well-structured output for applicant tracking systems
- **PDF Export** - Saves the customized resume in professional PDF format
- **Dual Interface** - Choose between CLI or Web UI based on your preference

## 📂 Folder Structure
resume-tailor/
├── README.md # Project overview
├── .env # API keys & config (not committed)
├── requirements.txt # Python dependencies
├── examples/ # Sample files for testing
│ ├── Sample_Resume.pdf
│ └── JD-Associate Consultant.pdf
├── src/
│ ├── main.py # CLI entry point
│ ├── app.py # Flask web app
│ └── resume_tailor/ # Core package
│ ├── init.py
│ ├── pipeline.py # Orchestrates the process
│ ├── parser.py # PDF/text parsing
│ ├── matcher.py # JD & resume keyword matching
│ ├── rewriter.py # AI-driven text rewriting
│ ├── emergent_adapter.py # Connects to Emergent.sh API
│ └── pdf_exporter.py # Generates final PDF
├── tests/
│ └── test_pipeline.py # Unit tests
└── scripts/
└── run_local.sh # Quick-start script


## ⚙️ How It Works

1. **Input**: Provide your resume (PDF/TXT) and job description (PDF/TXT)
2. **Parse**: System extracts raw text using pdfminer.six
3. **Match**: Identifies key skills, experiences, and phrases from the JD that match your resume
4. **Rewrite**: Uses Emergent.sh API to rewrite resume with targeted language
5. **Export**: Creates a polished, ATS-optimized PDF resume

## 🔑 Configuration

Create a `.env` file with these variables:
EMERGENT_API_KEY=sk_live_your_key_here
EMERGENT_API_URL=.....url.....
EMERGENT_MODEL=gpt-3.5-turbo

💻 Usage

CLI Mode

python src/main.py \
  --resume examples/Sample_Resume.pdf \
  --jd examples/JD-Associate\ Consultant.pdf \
  --use-llm

  
Web App Mode

python src/app.py
# Open browser at http://127.0.0.1:5000

🧪 Technologies Used
Python 3.10+
Flask (Web UI)
pdfminer.six (PDF parsing)
reportlab (PDF export)
Emergent.sh API (LLM resume rewriting)
python-dotenv (Environment variables)
pytest (Testing)

📌 Notes
Works with Emergent.sh free tier (just replace API key in .env)
Uses chat/completions endpoint with gpt-3.5-turbo by default (configurable)
Optimized for ATS compatibility with clean formatting
