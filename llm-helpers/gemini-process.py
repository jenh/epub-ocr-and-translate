# Quick and basic script to send PDF as context to Gemini 1.5 Pro
# with google-generativeai and ask some questions about it.

# Usage:
#
# python3 gemini-process.py /path/to/book_en.pdf "List all characters and their descriptions in a csv table"

from pathlib import Path
import hashlib
import google.generativeai as genai
import sys
import os
import PyPDF2

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

user_input = sys.argv[2]
pdf_file = sys.argv[1]

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

def extract_pdf_pages(pathname: str) -> list[str]:
  """Extracts text from a PDF and returns a list of pages.

  Args:
      pathname: Path to the PDF file.

  Returns:
      A list of strings representing the extracted text content from each page.
  """

  parts = []
  with open(pathname, 'rb') as pdf_file:
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    for page_num in range(len(pdf_reader.pages)):
      page = pdf_reader.pages[page_num]
      text = page.extract_text()
      parts.append(text)
  return parts

convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": extract_pdf_pages(pdf_file)
  },
])

convo.send_message(user_input)
print(convo.last.text)
