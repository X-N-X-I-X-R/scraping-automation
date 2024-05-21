from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from bidi.algorithm import get_display

# Register the font (use the actual path to the font file)
pdfmetrics.registerFont(TTFont('Nehama', 'nehama.ttf'))

# Create a PDF document
doc = SimpleDocTemplate("output.pdf", pagesize=letter)

# Create a paragraph style with the desired font and right alignment
style = ParagraphStyle('Nehama', parent=getSampleStyleSheet()['Normal'], fontName='Nehama', alignment=4) # 2 is for RTL alignment
allowed_chars = set(' !"#$%&\'()*+,-./0123456789:;<=>?@[\]^_`{|}~' + ''.join(chr(i) for i in range(0x0590, 0x05FF))) # type: ignore



# Open the text file and read its content
with open('translated.txt', 'r') as file:
  text = file.read()
  

# Filter the text to only include allowed characters
filtered_text = ''.join(c for c in text if c in allowed_chars)

# Apply get_display to the entire text, then split it into lines and create a paragraph for each line
rtl_text = get_display(filtered_text)
story = [Paragraph(get_display(line), style) for line in text.split('\n') if line.strip() != '']
doc.build(story)