from fastapi import APIRouter, HTTPException
from app.dto.resume_dto import ResumeRequest, ResumeResponse
from app.dto.resume_modify_dto import UpdateRequestDto,ResumeResponseDto
from app.services.api_service import process_repository
from concurrent.futures import ProcessPoolExecutor
import asyncio
import logging
import json
from app.services.stack_service import generate_techstack
from app.services.gpt_service import generate_aboutme, resume_update
from app.services.github_service import get_github_profile_and_repos
from app.config.settings import settings



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

    # # aboutme techstack 생성
    # aboutme_techstack = create_aboutme_techstack(project_summaries)
    

    
    repo_name = "/".join(str(request.selectedRepo[0]).rstrip('/').split('/')[-2:])

    
    # techstack 생성
    techstack = generate_techstack(settings.gh_token, repo_name)
    aboutme = generate_aboutme(settings.openai_api_key)
    
    print(aboutme)


    # 최종 이력서 응답 생성
    resume_response = ResumeResponse(
        projects=project_summaries,
        techStack=techstack,
        aboutMe=aboutme
        # aboutMe=aboutme_techstack.aboutMe
    )
    return resume_response




@router.put("/api/resumes", response_model=ResumeResponseDto)
async def update_resume(request: UpdateRequestDto):
    try:
        # 요청 데이터 확인
        print("=== Received Request Data ===")
        print(f"Selected Text: {request.selectedText}")
        print(f"Requirement: {request.requirement}")
        print(f"Resume Info: {request.resumeInfo.dict()}")

        # `resume_update` 호출 준비
        print("=== Calling `resume_update` ===")
        updated_resume = resume_update(
            openai_api_key=settings.openai_api_key,
            requirements=request.requirement,
            selected_text=request.selectedText,
            context_data=request.resumeInfo.dict()
        )

        # 업데이트된 결과 확인
        print("=== Updated Resume Data ===")
        print(updated_resume)

        # 업데이트된 결과 반환
        return updated_resume

    except Exception as e:
        print(f"Error in update_resume: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the resume.")