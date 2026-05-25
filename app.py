from fastapi import FastAPI, UploadFile, File, Form

from services.pdf_service import extract_text_from_pdf
from services.bedrock_service import analyze_resume
from services.s3_service import upload_file_to_s3
from schemas.resume_schema import ResumeResponse
app = FastAPI()

@app.get("/")
def home():
    return {
        "message": "Resume Matcher Running"
    }

@app.post(
    "/upload-resume",
    response_model=ResumeResponse
)
async def upload_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):

    # Read uploaded file content
    file_content = await resume.read()

    # Upload to S3
    s3_key = upload_file_to_s3(
        file_content,
        resume.filename
    )

    # Extract text directly from memory
    extracted_text = extract_text_from_pdf(
        file_content
    )

    # Analyze with Bedrock
    analysis = analyze_resume(
        extracted_text,
        job_description
    )

    return {
        "filename": resume.filename,
        "s3_key": s3_key,
        "analysis": analysis
    }