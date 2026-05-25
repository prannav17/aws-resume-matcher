from pydantic import BaseModel
from typing import List

class ResumeAnalysis(BaseModel):

    match_percentage: int
    matching_skills: List[str]
    missing_skills: List[str]
    summary: str


class ResumeResponse(BaseModel):

    filename: str
    s3_key: str
    analysis: ResumeAnalysis