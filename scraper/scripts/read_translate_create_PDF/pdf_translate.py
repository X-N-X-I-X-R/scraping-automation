import textwrap
from deep_translator import GoogleTranslator
from PyPDF2 import PdfReader




def extract_text_from_pdf(file_path):
  pdf = PdfReader(file_path)
  text = ''
  for page in pdf.pages:
    text += page.extract_text()
  return text

def translate_text(text):
  # Translate the text in chunks of 4900 characters
  translated = ""
  for chunk in textwrap.wrap(text, 4900):  # Break the text into chunks of 4900 characters
    translated_chunk = GoogleTranslator(source='auto', target='iw').translate(chunk)
    translated_chunk = translated_chunk.replace('.', '.\n')  # Add a new line after each period
    translated += translated_chunk
  return translated



# Use the functions
text = extract_text_from_pdf('acn.pdf')
translated = translate_text(text)

# Write the translated text to a text file
with open('translated.txt', 'w') as f:
  f.write(translated)






