import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.colors import black

def generate_pdf_resume(text, output_path):
    """
    Generates a professional PDF resume with proper formatting similar to the example.
    """
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Set margins
    x_margin = inch * 0.75
    y_margin = inch * 0.75
    y_position = height - y_margin
    
    # Create styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=16,
        leading=18,
        alignment=TA_LEFT,
        spaceAfter=12,
        textColor=black
    )
    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=12,
        leading=14,
        alignment=TA_LEFT,
        spaceBefore=12,
        spaceAfter=6,
        textColor=black
    )
    content_style = ParagraphStyle(
        'Content',
        parent=styles['BodyText'],
        fontSize=10,
        leading=12,
        alignment=TA_LEFT,
        spaceAfter=6,
        textColor=black
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['BodyText'],
        fontSize=10,
        leading=12,
        leftIndent=10,
        bulletIndent=0,
        spaceAfter=4,
        textColor=black
    )
    
    # Process the text line by line
    lines = text.splitlines()
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # Check for section headers (lines that are all caps or have special formatting)
        if line.startswith('# '):
            # Title line
            title = line[2:].strip()
            p = Paragraph(title, title_style)
            p.wrapOn(c, width - 2*x_margin, height)
            p.drawOn(c, x_margin, y_position - p.height)
            y_position -= p.height + 12
            
            # Draw a horizontal line under the title
            c.setStrokeColor(black)
            c.setLineWidth(0.5)
            c.line(x_margin, y_position, width - x_margin, y_position)
            y_position -= 12
        elif line.startswith('## '):
            # Section header
            section = line[3:].strip()
            p = Paragraph(f'<b>{section}</b>', section_style)
            p.wrapOn(c, width - 2*x_margin, height)
            p.drawOn(c, x_margin, y_position - p.height)
            y_position -= p.height + 6
            current_section = section
        elif line.startswith('- '):
            # Bullet point
            bullet = line[2:].strip()
            p = Paragraph(f'• {bullet}', bullet_style)
            p.wrapOn(c, width - 2*x_margin - 10, height)
            p.drawOn(c, x_margin + 10, y_position - p.height)
            y_position -= p.height
        else:
            # Regular content
            if '|' in line and current_section in ['EDUCATION', 'INTERNSHIP EXPERIENCE']:
                # Format as two-column layout for education and experience
                parts = [part.strip() for part in line.split('|')]
                if len(parts) == 2:
                    c.setFont("Helvetica-Bold", 10)
                    c.drawString(x_margin, y_position - 10, parts[0])
                    c.setFont("Helvetica", 10)
                    c.drawRightString(width - x_margin, y_position - 10, parts[1])
                    y_position -= 14
                else:
                    p = Paragraph(line, content_style)
                    p.wrapOn(c, width - 2*x_margin, height)
                    p.drawOn(c, x_margin, y_position - p.height)
                    y_position -= p.height
            else:
                p = Paragraph(line, content_style)
                p.wrapOn(c, width - 2*x_margin, height)
                p.drawOn(c, x_margin, y_position - p.height)
                y_position -= p.height
        
        # Check for page break
        if y_position <= y_margin:
            c.showPage()
            y_position = height - y_margin
            current_section = None
    
    c.save()
    return output_path
