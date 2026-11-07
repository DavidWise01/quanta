#!/usr/bin/env python3
"""Build the complete QUANTA manuscript from the canonical Markdown chapter sources."""
from __future__ import annotations
import re
from pathlib import Path
from xml.sax.saxutils import escape
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.shared import Inches, Pt, RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "book" / "chapters"
OUT = ROOT / "book" / "QUANTA_The_Wordle_of_Space_Complete_32_5.docx"
FILES = sorted(SRC.glob("*.md"),key=lambda p:(float(p.name[:2]) if p.name[:2].isdigit() else 999,1 if p.name.startswith("32-5") else 0))
assert len(FILES)==33, f"Expected 33 chapter files, found {len(FILES)}: {[p.name for p in FILES]}"
assert FILES[-1].name=="32-5-the-half-step.md"
C=RGBColor(34,66,73)
M=RGBColor(58,115,121)
D=RGBColor(68,78,86)

def style_run(r,kind):
    r.font.name="Consolas" if kind=="code" else "Georgia"
    if kind=="code": r.font.size=Pt(9);r.font.color.rgb=M

def add_inline(p,s):
    # Preserve backticks, emphasis and bold while leaving ordinary markdown prose readable.
    parts=re.split(r'(\`[^\`]+\`|\*\*[^*]+\*\*|\*[^*]+\*)',s)
    for part in parts:
        if not part: continue
        if part.startswith("\`") and part.endswith("\`"):
            r=p.add_run(part[1:-1]);style_run(r,"code")
        elif part.startswith("**") and part.endswith("**"):
            r=p.add_run(part[2:-2]);r.bold=True
        elif part.startswith("*") and part.endswith("*"):
            r=p.add_run(part[1:-1]);r.italic=True
        else:p.add_run(part)

def bookmark(p,i):
    start=OxmlElement("w:bookmarkStart");start.set(qn("w:id"),str(i));start.set(qn("w:name"),f"chapter_{i}")
    end=OxmlElement("w:bookmarkEnd");end.set(qn("w:id"),str(i))
    p._p.insert(0,start);p._p.append(end)

def linked_toc_entry(p,title,i):
    link=OxmlElement("w:hyperlink");link.set(qn("w:anchor"),f"chapter_{i}")
    r=OxmlElement("w:r");pr=OxmlElement("w:rPr")
    col=OxmlElement("w:color");col.set(qn("w:val"),"347880");pr.append(col)
    r.append(pr);t=OxmlElement("w:t");t.text=title;r.append(t);link.append(r);p._p.append(link)

def add_page_field(par):
    par.alignment=WD_ALIGN_PARAGRAPH.CENTER
    r=par.add_run()
    a=OxmlElement("w:fldChar");a.set(qn("w:fldCharType"),"begin");r._r.append(a)
    instr=OxmlElement("w:instrText");instr.set(qn("xml:space"),"preserve");instr.text=" PAGE ";r._r.append(instr)
    b=OxmlElement("w:fldChar");b.set(qn("w:fldCharType"),"end");r._r.append(b)

def render_markdown(doc,raw):
    lines=raw.splitlines();i=0;in_code=False;block=[]
    def flush_code():
        nonlocal block
        if not block:return
        p=doc.add_paragraph(style="Code Block")
        p.paragraph_format.keep_together=True
        r=p.add_run("\n".join(block));r.font.name="Consolas";r.font.size=Pt(9)
        block=[]
    while i<len(lines):
        line=lines[i];strip=line.strip()
        if strip.startswith("\`\`\`"):
            if in_code:flush_code()
            in_code=not in_code;i+=1;continue
        if in_code:block.append(line);i+=1;continue
        if not strip:i+=1;continue
        if strip=="---":doc.add_paragraph(style="Divider");i+=1;continue
        if strip.startswith("|") and i+1<len(lines) and re.fullmatch(r'[\s|:\-]+',lines[i+1]):
            headers=[x.strip() for x in strip.strip("|").split("|")];i+=2
            rows=[]
            while i<len(lines) and lines[i].lstrip().startswith("|"):
                rows.append([x.strip() for x in lines[i].strip().strip("|").split("|")]);i+=1
            tab=doc.add_table(rows=1,cols=len(headers));tab.style="Light Shading Accent 1";tab.alignment=WD_TABLE_ALIGNMENT.CENTER
            for c,v in zip(tab.rows[0].cells,headers):c.text=v
            for values in rows:
                cells=tab.add_row().cells
                for j in range(len(headers)):cells[j].text=values[j] if j<len(values) else ""
            for row in tab.rows:
                for cell in row.cells:
                    cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                    for p in cell.paragraphs:
                        for r in p.runs:r.font.size=Pt(8)
            doc.add_paragraph();continue
        m=re.match(r'^(#{1,5})\s+(.*)',strip)
        if m:
            rank=len(m.group(1))
            p=doc.add_paragraph(style="Heading "+str(min(rank,4)))
            add_inline(p,m.group(2));i+=1;continue
        if strip.startswith("> "):
            p=doc.add_paragraph(style="Quote");add_inline(p,strip[2:]);i+=1;continue
        if re.match(r'^\s*[-*]\s+',line):
            p=doc.add_paragraph(style="List Bullet");add_inline(p,re.sub(r'^\s*[-*]\s+','',line));i+=1;continue
        if re.match(r'^\s*\d+\.\s+',line):
            p=doc.add_paragraph(style="List Number");add_inline(p,re.sub(r'^\s*\d+\.\s+','',line));i+=1;continue
        # Markdown hard line breaks are merged into one paragraph.
        para=[strip]
        while i+1<len(lines):
            next_=lines[i+1].strip()
            if not next_ or next_.startswith(("#","|",">","\`\`\`")) or next_=="---" or re.match(r'^([-*]|\d+\.)\s+',next_):break
            i+=1;para.append(next_)
        p=doc.add_paragraph();add_inline(p," ".join(para));i+=1
    flush_code()

doc=Document()
sec=doc.sections[0];sec.top_margin=Inches(.84);sec.bottom_margin=Inches(.75);sec.left_margin=Inches(.95);sec.right_margin=Inches(.9)
styles=doc.styles
styles["Normal"].font.name="Georgia";styles["Normal"].font.size=Pt(10.5);styles["Normal"].font.color.rgb=D
styles["Normal"].paragraph_format.space_after=Pt(8);styles["Normal"].paragraph_format.line_spacing=1.16
for name,size in [("Heading 1",20),("Heading 2",14),("Heading 3",11.5),("Heading 4",10.5)]:
    s=styles[name];s.font.name="Aptos Display";s.font.size=Pt(size);s.font.bold=True;s.font.color.rgb=C
    s.paragraph_format.space_before=Pt(16 if name=="Heading 1" else 10)
    s.paragraph_format.space_after=Pt(6)
    s.paragraph_format.keep_with_next=True
from docx.enum.style import WD_STYLE_TYPE
for name in ["Code Block","Divider","Quote"]:
    if name not in styles:styles.add_style(name,WD_STYLE_TYPE.PARAGRAPH)
styles["Code Block"].font.name="Consolas";styles["Code Block"].font.size=Pt(9)
styles["Code Block"].paragraph_format.left_indent=Inches(.27)
styles["Code Block"].paragraph_format.space_after=Pt(10)
styles["Quote"].font.name="Georgia";styles["Quote"].font.italic=True
styles["Quote"].paragraph_format.left_indent=Inches(.35)
styles["Divider"].paragraph_format.space_before=Pt(3)
styles["Divider"].paragraph_format.space_after=Pt(3)
# Cover
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(110)
r=p.add_run("QUANTA");r.bold=True;r.font.name="Aptos Display";r.font.size=Pt(48);r.font.color.rgb=C
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
r=p.add_run("THE WORDLE OF SPACE");r.font.name="Aptos Display";r.font.size=Pt(20);r.font.color.rgb=M
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(48)
r=p.add_run("[ .|.|.|.|. ]");r.font.name="Consolas";r.font.size=Pt(23)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(45)
r=p.add_run("David Lee Wise");r.font.name="Georgia";r.font.size=Pt(16)
p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Complete manuscript · 32 chapters + the 32.5 coda\nNovember 2026")
doc.add_page_break()
toc=doc.add_paragraph("CONTENTS",style="Heading 1")
chapters=[]
for path in FILES:
    text=path.read_text(encoding="utf-8")
    first=next((line.lstrip("# ").strip() for line in text.splitlines() if line.startswith("# ")),path.stem)
    chapters.append((path,first,text))
for i,(_,name,_) in enumerate(chapters,1):
    p=doc.add_paragraph();p.paragraph_format.space_after=Pt(4);linked_toc_entry(p,name,i)
doc.add_page_break()
for i,(path,title,content) in enumerate(chapters,1):
    # Attach the bookmark to the actual chapter title, not a ghost paragraph.
    p=doc.add_paragraph(style="Heading 1");add_inline(p,title);bookmark(p,i)
    # Remove duplicated leading markdown H1, but retain subtitle and full remaining manuscript.
    body=re.sub(r'\A# .*\n','',content,count=1)
    render_markdown(doc,body)
    if i<len(chapters):doc.add_page_break()
header=sec.header.paragraphs[0];header.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=header.add_run("QUANTA · THE WORDLE OF SPACE");r.font.size=Pt(8);r.font.color.rgb=M
add_page_field(sec.footer.paragraphs[0])
doc.core_properties.title="QUANTA — The Wordle of Space"
doc.core_properties.author="David Lee Wise"
doc.core_properties.subject="Complete 32.5-chapter manuscript"
OUT.parent.mkdir(parents=True,exist_ok=True)
doc.save(OUT)
print(f"Saved {OUT}, {len(chapters)} chapter files, {sum(len(x[2].split()) for x in chapters)} source words, {OUT.stat().st_size} bytes")
