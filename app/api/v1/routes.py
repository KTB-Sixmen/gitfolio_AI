from fastapi import APIRouter, HTTPException
from app.dto.resume_dto import ResumeRequest, ResumeResponse
from app.dto.resume_modify_dto import UpdateRequestDto,ResumeResponseDto
from app.services.api_service import process_repository
from concurrent.futures import ProcessPoolExecutor
from app.services.resume_templates import generate_resume_response
import asyncio
import logging
import json
from app.services.stack_service import generate_techstack
from app.services.gpt_service import generate_aboutme, resume_update, generate_role_and_task, generate_trouble_shooting, generate_star_summary
from app.services.github_service import get_github_profile_and_repos
from app.config.settings import settings
from fastapi.responses import JSONResponse



router = APIRouter()

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
    resume_response = generate_resume_response(
        # template=request.template,
        project_summaries=project_summaries,
        techstack=techstack,
        aboutme=aboutme
    )
    print("==================")
    print(resume_response)
    
    return resume_response
    # return JSONResponse(content=resume_response.dict())



@router.put("/api/ai/resumes", response_model=ResumeResponseDto)
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
    
    # 최종 이력서 응답 생성
    resume_response = ResumeResponse(
        projects=project_summaries,
        techStack=techstack,
        aboutMe=aboutme
    )
    return resume_response

# # 이력서 생성 api 2안
# @router.post("/api/ai/resumes", response_model=ResumeResponse)
# async def generate_resume(request: ResumeRequest):
#     logging.basicConfig(level=logging.INFO)

#     # 각 레포지토리 요약을 멀티프로세싱으로 처리
#     with ProcessPoolExecutor() as executor:
#         loop = asyncio.get_event_loop()
#         tasks = [
#             loop.run_in_executor(executor, process_repository, repo_url, request.githubID, request.githubName, request.requirements)
#             for repo_url in request.selectedRepo
#         ]
#         try:
#             # 실패 시 예외를 발생시키고 에러 메시지를 리턴
#             project_summaries = await asyncio.gather(*tasks)

#         except Exception as e:
#             logging.error(f"Error processing repositories: {e}")
#             return {"error": f"Error processing repositories: {str(e)}"}

#     # 공통 데이터 생성
#     repo_name = "/".join(str(request.selectedRepo[0]).rstrip('/').split('/')[-2:])
#     techstack = generate_techstack(settings.gh_token, repo_name)
#     aboutme = generate_aboutme(settings.openai_api_key)

#     # 템플릿에 맞는 데이터 준비
#     role_and_task = None
#     trouble_shooting = None
#     star_summary = None

#     if request.template == "basic":
#         role_and_task = generate_role_and_task(
#             openai_api_key=settings.openai_api_key,
#             code_summary=code_summary,
#             pr_summary=pr_summary,
#             commit_summary=commit_summary,
#             requirements=request.requirements
#         ).roleAndTask

#     elif request.template == "gitfolio":
#         role_and_task = generate_role_and_task(
#             openai_api_key=settings.openai_api_key,
#             code_summary="code_summary_content",
#             pr_summary="pr_summary_content",
#             commit_summary="commit_summary_content",
#             requirements=request.requirements
#         ).roleAndTask
#         trouble_shooting = generate_trouble_shooting(
#             openai_api_key=settings.openai_api_key,
#             code_summary="code_summary_content",
#             pr_summary="pr_summary_content",
#             commit_summary="commit_summary_content",
#             requirements=request.requirements
#         ).troubleShooting

#     elif request.template == "star":
#         star_summary = generate_star_summary(
#             openai_api_key=settings.openai_api_key,
#             repo_data="repo_data_content",
#             issues_data="issues_data_content",
#             pr_summary="pr_summary_content",
#             commit_summary="commit_summary_content",
#             pr_data="pr_data_content",
#             commits_data="commits_data_content",
#             requirements=request.requirements
#         ).projectDescription

#     # 최종 이력서 응답 생성
#     resume_response = generate_resume_response(
#         template=request.template,
#         project_summaries=project_summaries,
#         techstack=techstack,
#         aboutme=aboutme,
#         role_and_task=role_and_task,
#         trouble_shooting=trouble_shooting,
#         star_summary=star_summary
#     )

#     return resume_response