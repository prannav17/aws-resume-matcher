import PyPDF2
from io import BytesIO

def extract_text_from_pdf(file_content):

    extracted_text = ""

    pdf_stream = BytesIO(file_content)

    reader = PyPDF2.PdfReader(pdf_stream)

    for page in reader.pages:

        text = page.extract_text()

        if text:
            extracted_text += text + "\n"

    return extracted_text