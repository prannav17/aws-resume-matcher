from services.textract_service import extract_text_from_document
from dotenv import load_dotenv

import os

load_dotenv()

BUCKET_NAME = os.getenv("BUCKET_NAME")

document_name = "Pranav.pdf"

text = extract_text_from_document(
    BUCKET_NAME,
    document_name
)

print(text)