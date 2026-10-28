import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    kwargs can contain top, bottom, left, right.
    Value is dict with val, color, sz, space.
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = parse_xml(f'<{tag} {nsdecls("w")} w:val="{edge_data.get("val","single")}" w:sz="{edge_data.get("sz","4")}" w:space="0" w:color="{edge_data.get("color","auto")}"/>')
            tcBorders.append(element)
    tcPr.append(tcBorders)

def add_header_footer(doc):
    for s in doc.sections:
        s.different_first_page_header_footer = True
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("AQUANTIS: Water Quality Prediction Framework | Mini-Project Report")
        hrun.font.name = "Arial"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(148, 163, 184)
        
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Department of Computer Science & Engineering | Academic Lab Evaluation")
        frun.font.name = "Arial"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(148, 163, 184)

def format_paragraph(p, space_before=0, space_after=6, line_spacing=1.15):
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing

def add_heading_1(doc, text):
    h = doc.add_paragraph()
    format_paragraph(h, space_before=16, space_after=6)
    run = h.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(11, 46, 60) # Deep Midnight Navy
    return h

def add_heading_2(doc, text):
    h = doc.add_paragraph()
    format_paragraph(h, space_before=12, space_after=4)
    run = h.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(8, 127, 140) # Rich Teal
    return h

def add_heading_3(doc, text):
    h = doc.add_paragraph()
    format_paragraph(h, space_before=8, space_after=3)
    run = h.add_run(text)
    run.font.name = "Arial"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(30, 41, 59)
    return h

def add_body_p(doc, text, bold_prefix="", italic=False):
    p = doc.add_paragraph()
    format_paragraph(p, space_before=0, space_after=6, line_spacing=1.15)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.italic = italic
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_bullet(doc, text, bold_prefix=""):
    p = doc.add_paragraph(style='List Bullet')
    format_paragraph(p, space_before=0, space_after=3, line_spacing=1.15)
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(11)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_callout(doc, text, bold_title=""):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "F0FDF4") # Subtle mint/light teal
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    set_cell_border(cell, 
                    left={"val": "single", "sz": "24", "color": "087F8C"},
                    top={"val": "single", "sz": "4", "color": "D1FAE5"},
                    bottom={"val": "single", "sz": "4", "color": "D1FAE5"},
                    right={"val": "single", "sz": "4", "color": "D1FAE5"})
    p = cell.paragraphs[0]
    format_paragraph(p, space_before=0, space_after=0, line_spacing=1.15)
    if bold_title:
        r_title = p.add_run(bold_title + "\n")
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(10.5)
        r_title.font.bold = True
        r_title.font.color.rgb = RGBColor(7, 91, 104)
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(15, 23, 42)
    p_after = doc.add_paragraph()
    format_paragraph(p_after, space_before=0, space_after=4)

def add_table_data(doc, headers, data, col_widths=None, alignment=WD_TABLE_ALIGNMENT.CENTER):
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = alignment
    table.autofit = False
    
    # Header Row
    hdr_row = table.rows[0]
    for i, title in enumerate(headers):
        cell = hdr_row.cells[i]
        set_cell_background(cell, "0B2E3C") # Dark Navy
        set_cell_margins(cell, top=120, bottom=120, left=140, right=140)
        set_cell_border(cell, 
                        top={"val": "single", "sz": "6", "color": "0B2E3C"},
                        bottom={"val": "single", "sz": "12", "color": "087F8C"},
                        left={"val": "none"}, right={"val": "none"})
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if i > 0 else WD_ALIGN_PARAGRAPH.LEFT
        format_paragraph(p, space_before=0, space_after=0)
        run = p.add_run(title)
        run.font.name = "Arial"
        run.font.size = Pt(9.5)
        run.font.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    # Data Rows
    for r_idx, row_values in enumerate(data):
        row = table.rows[r_idx + 1]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_values):
            cell = row.cells[c_idx]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            set_cell_border(cell, 
                            top={"val": "single", "sz": "4", "color": "E2E8F0"},
                            bottom={"val": "single", "sz": "4", "color": "E2E8F0"},
                            left={"val": "none"}, right={"val": "none"})
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if c_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
            format_paragraph(p, space_before=0, space_after=0)
            run = p.add_run(str(val))
            run.font.name = "Calibri"
            run.font.size = Pt(9.5)
            run.font.color.rgb = RGBColor(15, 23, 42)
            if c_idx == 0:
                run.font.bold = True
                
    if col_widths:
        for r in table.rows:
            for c_idx, w in enumerate(col_widths):
                r.cells[c_idx].width = Inches(w)
                
    p_after = doc.add_paragraph()
    format_paragraph(p_after, space_before=0, space_after=6)
    return table

def add_figure_image(doc, img_path, caption, width_in=5.8):
    if Path(img_path).exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_paragraph(p_img, space_before=6, space_after=3)
        run = p_img.add_run()
        run.add_picture(str(img_path), width=Inches(width_in))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_paragraph(p_cap, space_before=0, space_after=8)
        run_cap = p_cap.add_run(caption)
        run_cap.font.name = "Calibri"
        run_cap.font.size = Pt(9)
        run_cap.font.italic = True
        run_cap.font.color.rgb = RGBColor(71, 85, 105)
    else:
        print(f"Warning: Figure image not found at {img_path}")

print("Report generator library defined successfully.")
