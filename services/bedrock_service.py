
import json
import os
import re
import boto3
from dotenv import load_dotenv

load_dotenv()

client = boto3.client(
    "bedrock-runtime",
    region_name=os.getenv("AWS_REGION")
)

def analyze_resume(resume_text, job_description):

    prompt = f"""
You are a professional AI resume evaluator.

Compare the resume with the job description.

Return ONLY valid JSON.
Do not add explanations.
Do not use markdown.
Do not wrap response in triple backticks.

Example format:

{{
    "match_percentage": 85,
    "matching_skills": [
        "Python",
        "AWS",
        "FastAPI"
    ],
    "missing_skills": [
        "Kubernetes"
    ],
    "summary": "Strong backend candidate with cloud experience."
}}

Job Description:
{job_description}

Resume:
{resume_text}
"""

    body = {
        "prompt": prompt,
        "max_gen_len": 400,
        "temperature": 0.1
    }

    response = client.invoke_model(
        modelId="meta.llama3-8b-instruct-v1:0",
        body=json.dumps(body),
        contentType="application/json",
        accept="application/json"
    )

    response_body = json.loads(
        response["body"].read()
    )

    print("BEDROCK RESPONSE:")
    print(json.dumps(response_body, indent=2))

    generated_text = response_body.get("generation", "")

    print("GENERATED TEXT:")
    print(repr(generated_text))

    try:

        # Extract JSON safely
        match = re.search(r"\{.*\}", generated_text, re.DOTALL)

        if not match:
            raise ValueError("No JSON found")

        json_text = match.group()

        parsed_response = json.loads(json_text)

        return parsed_response

    except Exception as e:

        return {
            "match_percentage": 0,
            "matching_skills": [],
            "missing_skills": [],
            "summary": f"Failed to parse model response: {str(e)}"
        }
