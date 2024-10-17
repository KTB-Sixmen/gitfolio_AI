from fastapi import APIRouter
from app.services.github_service import fetch_github_info
from app.services.ai_service import generate_resume

router = APIRouter()

#  dto에 맞게 재수정할것
@router.post("/generate-resume")
async def generate_resume_from_github(github_username: str):
    github_data = fetch_github_info(github_username)
    resume = generate_resume(github_data)
    return {"resume": resume}
    