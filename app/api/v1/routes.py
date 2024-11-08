from fastapi import APIRouter
from app.dto.resume_dto import ResumeRequest, ResumeResponse
from app.services.api_service import process_repository, create_aboutme_techstack
from concurrent.futures import ProcessPoolExecutor
import asyncio
import logging

router = APIRouter()

# 이력서 생성 api
@router.post("/api/resumes", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    logging.basicConfig(level=logging.INFO)

    # 각 레포지토리 요약을 멀티프로세싱으로 처리
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_repository, repo_url, request.githubID, request.githubName, request.requirements)
            for repo_url in request.selectedRepo
        ]
        try:
            # 실패 시 예외를 발생시키고 에러 메시지를 리턴
            project_summaries = await asyncio.gather(*tasks)

        except Exception as e:
            logging.error(f"Error processing repositories: {e}")
            return {"error": f"Error processing repositories: {str(e)}"}

    # aboutme techstack 생성
    aboutme_techstack = create_aboutme_techstack(project_summaries)


    # 최종 이력서 응답 생성
    resume_response = ResumeResponse(
        projects=project_summaries,
        techStack=aboutme_techstack.techStack,
        aboutMe=aboutme_techstack.aboutMe
    )
    return resume_response
