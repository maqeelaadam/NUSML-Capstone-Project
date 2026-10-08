"""Render the four capstone reports from their Markdown sources."""
import logging
from pathlib import Path
logger=logging.getLogger(__name__)
if __name__ == "__main__":
 logging.basicConfig(level=logging.INFO,format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",handlers=[logging.StreamHandler(),logging.FileHandler(Path(__file__).resolve().parents[1]/"report_rendering.log",encoding="utf-8")])
from pathlib import Path
from xml.sax.saxutils import escape
import re
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,KeepTogether,PageBreak
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
root=Path(__file__).resolve().parents[1]
styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='ReportTitle',fontName='Helvetica-Bold',fontSize=18,leading=22,spaceAfter=14,textColor=colors.black))
styles.add(ParagraphStyle(name='ReportHeading',fontName='Helvetica-Bold',fontSize=11.5,leading=15,spaceBefore=10,spaceAfter=6,keepWithNext=True,textColor=colors.black))
styles.add(ParagraphStyle(name='ReportBody',fontName='Helvetica',fontSize=10.3,leading=14,spaceAfter=7))
styles.add(ParagraphStyle(name='ReportCell',fontName='Helvetica',fontSize=8,leading=10))
def clean(text):
 text=text.replace('–','-').replace('—','-').replace('’',"'").replace('“','"').replace('”','"')
 return escape(text.replace('`',''))
def footer(canvas,doc):
 canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#555555'))
 canvas.drawString(44,30,'NUS AMLDS Capstone | 8 October 2026 | Historical analysis and simulation')
 canvas.drawRightString(A4[0]-44,30,str(doc.page))
for path in [root/'capstone_part1/reports/insights_report.md',root/'capstone_part2/reports/methodology_report.md',root/'capstone_part3/reports/final_report.md',root/'capstone_part3/reports/bias_fairness_report.md']:
 lines=path.read_text().splitlines();story=[];i=0
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith('|'):
   rows=[]
   while i<len(lines) and lines[i].strip().startswith('|'):
    cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
    if not all(re.fullmatch(r'[- :]+',x) for x in cells):rows.append([Paragraph(clean(x),styles['ReportCell']) for x in cells])
    i+=1
   n=len(rows[0]);width=A4[0]-88
   widths=[width*.37]+[width*.63/(n-1)]*(n-1) if n==4 else [width*.32]+[width*.68/(n-1)]*(n-1)
   t=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
   t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8edf2')),('GRID',(0,0),(-1,-1),.4,colors.HexColor('#d9d9d9')),('VALIGN',(0,0),(-1,-1),'MIDDLE'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
   story.extend([t,Spacer(1,9)]);continue
  if line.startswith('# '):story.append(Paragraph(clean(line[2:]),styles['ReportTitle']))
  elif line.startswith('## '):
   if (path.name=='insights_report.md' and line=='## Statistics and weather probabilities') or (path.name=='methodology_report.md' and line=='## Feature engineering and figures') or (path.name=='bias_fairness_report.md' and line=='## Governance and appropriate oversight'):
    story.append(PageBreak())
   if path.name=='final_report.md' and line=='## Explainability and advanced technique':
    block=[Paragraph(clean(line[3:]),styles['ReportHeading'])]
    j=i+1
    paragraph=[]
    while j<len(lines) and not lines[j].startswith('## '):
     if lines[j].strip():paragraph.append(lines[j].strip())
     elif paragraph:
      block.append(Paragraph(clean(' '.join(paragraph)),styles['ReportBody']));paragraph=[]
     j+=1
    if paragraph:block.append(Paragraph(clean(' '.join(paragraph)),styles['ReportBody']))
    story.append(KeepTogether(block));i=j;continue
   story.append(Paragraph(clean(line[3:]),styles['ReportHeading']))
  else:
   paragraph=[line]
   while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].startswith(('#','|')):
    i+=1;paragraph.append(lines[i].strip())
   story.append(Paragraph(clean(' '.join(paragraph)),styles['ReportBody']))
  i+=1
 output=path.with_suffix('.pdf')
 SimpleDocTemplate(str(output),pagesize=A4,rightMargin=44,leftMargin=44,topMargin=42,bottomMargin=48,title=lines[0].lstrip('# '),author='NUS AMLDS Capstone Project').build(story,onFirstPage=footer,onLaterPages=footer)
 logger.info("Saved report %s",output)
