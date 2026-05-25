import boto3
import os

from dotenv import load_dotenv

load_dotenv()

textract = boto3.client(
    "textract",
    region_name=os.getenv("AWS_REGION")
)

def extract_text_from_document(bucket, document_name):

    response = textract.detect_document_text(
        Document={
            "S3Object": {
                "Bucket": bucket,
                "Name": document_name
            }
        }
    )

    extracted_text = ""

    for item in response["Blocks"]:

        if item["BlockType"] == "LINE":
            extracted_text += item["Text"] + "\n"

    return extracted_text