from fastapi import APIRouter, HTTPException
from app.dto.resume_dto import ResumeRequest, ResumeResponse, BasicDto, freedom_dto, gitfolio_dto, star_dto
from app.dto.resume_modify_dto import UpdateRequestDto,ResumeResponseDto
from app.services.api_service import process_repository, create_repo_start_end_date
from concurrent.futures import ProcessPoolExecutor
import asyncio
import logging
import json
from app.services.stack_service import generate_techstack
from app.services.gpt_service import generate_aboutme, resume_update, generate_project_title, generate_role_and_task
from app.services.github_service import get_github_profile_and_repos
from app.config.settings import settings



router = APIRouter()
# 기존 코드 백업용
# 이력서 생성 api
@router.post("/api/ai/resumes", response_model=ResumeResponse)
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

    # 레포 이름
    repo_name = "/".join(str(request.selectedRepo[0]).rstrip('/').split('/')[-2:])
    
    # techstack 생성
    techstack = generate_techstack(settings.gh_token, repo_name)
    aboutme = generate_aboutme(settings.openai_api_key)
    
    # # 선택적 구성 생성   
    # role_and_task = generate_role_and_task(settings.openai_api_key)
    # trouble_shooting = generate_trouble_shooting(settings.openai_api_key)
    # star = generate_star_summary(settings.openai_api_key)
    
    
    print("==========") 
    print(aboutme)

    # 최종 이력서 응답 생성
    resume_response = ResumeResponse(
        template=request.template,
        project_summaries=project_summaries,
    )
    print("==================")
    print(resume_response)
    
    return resume_response
    # return JSONResponse(content=resume_response.dict())