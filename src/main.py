# src/main.py
from dotenv import load_dotenv
load_dotenv()

import click
from resume_tailor.pipeline import generate_custom_resume_from_files

@click.group()
def cli():
    pass

@cli.command("run")
@click.option("--resume", required=True, help="Path to resume PDF or TXT")
@click.option("--jd", required=True, help="Path to JD PDF or TXT")
@click.option("--out", default="customized_resume.txt", help="Output path for customized resume (TXT)")
@click.option("--use-llm", is_flag=True, default=False, help="Enable optional Emergent LLM polish if configured")
def run(resume, jd, out, use_llm):
    """
    Run the pipeline using files (PDF or TXT). Outputs a TXT customized resume.
    """
    result = generate_custom_resume_from_files(resume, jd, use_llm=use_llm)
    with open(out, "w", encoding="utf-8") as f:
        f.write(result)
    click.echo(f"Wrote customized resume to {out}")

if __name__ == "__main__":
    cli()
