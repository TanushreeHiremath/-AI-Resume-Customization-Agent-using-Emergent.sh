#!/usr/bin/env bash
# simple runner for Unix-like systems
python -m src.main run \
  --resume examples/Sample_Resume.pdf \
  --jd "examples/JD-Associate Consultant.pdf" \
  --out out_customized_resume.txt \
  --use-llm
echo "Output -> out_customized_resume.txt"
