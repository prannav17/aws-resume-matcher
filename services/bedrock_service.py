import boto3
import json
import os

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

    formatted_prompt = f"""
<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a helpful AI assistant.

<|eot_id|><|start_header_id|>user<|end_header_id|>

{prompt}

<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

    body = {
        "prompt": formatted_prompt,
        "max_gen_len": 400,
        "temperature": 0.3
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

    generated_text = response_body["generation"]

    try:
        parsed_response = json.loads(generated_text)
        return parsed_response

    except Exception:
        return {
            "raw_response": generated_text
        }