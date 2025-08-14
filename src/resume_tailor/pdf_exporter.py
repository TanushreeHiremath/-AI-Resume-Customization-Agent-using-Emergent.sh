# src/resume_tailor/pdf_exporter.py
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

def generate_pdf_resume(text, output_path):
    """
    Generates a simple, ATS-friendly PDF with plain text from `text`.
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    # Basic settings
    x_margin = inch * 0.75
    y_margin = inch * 0.75
    y_position = height - y_margin

    c.setFont("Helvetica-Bold", 12)
    # Title: first line if present — otherwise we'll print top lines as normal
    lines = text.splitlines()
    # If first line is the title, print bold a bit larger
    if lines:
        c.drawString(x_margin, y_position, lines[0])
        y_position -= 16
        # draw a line under title
        c.setLineWidth(0.5)
        c.line(x_margin, y_position + 6, width - x_margin, y_position + 6)
        y_position -= 8
        # start rest from lines[1:]
        rest = lines[1:]
    else:
        rest = []

    c.setFont("Helvetica", 10)
    for line in rest:
        # ensure we don't overflow margins
        if y_position <= y_margin:
            c.showPage()
            y_position = height - y_margin
            c.setFont("Helvetica", 10)
        # handle long lines: wrap roughly by width
        max_chars = 95  # approximate; adjust if needed
        if len(line) <= max_chars:
            c.drawString(x_margin, y_position, line)
            y_position -= 12
        else:
            # naive wrap
            while len(line) > 0:
                chunk = line[:max_chars]
                # try to break at last space
                if len(line) > max_chars:
                    sp = chunk.rfind(" ")
                    if sp > 20:
                        chunk = line[:sp]
                c.drawString(x_margin, y_position, chunk)
                y_position -= 12
                line = line[len(chunk):].lstrip()
                if y_position <= y_margin:
                    c.showPage()
                    y_position = height - y_margin
                    c.setFont("Helvetica", 10)
    c.save()
    return output_path
