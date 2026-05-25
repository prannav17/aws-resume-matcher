import boto3
import uuid
import os

from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

s3 = boto3.client("s3")

BUCKET_NAME = os.getenv("BUCKET_NAME")

def upload_file_to_s3(file_content, filename):

    unique_filename = f"{uuid.uuid4()}-{filename}"

    file_stream = BytesIO(file_content)

    s3.upload_fileobj(
        file_stream,
        BUCKET_NAME,
        unique_filename
    )

    return unique_filename