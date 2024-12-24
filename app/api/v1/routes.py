from fastapi import APIRouter, HTTPException
from app.dto.resume_dto import ResumeRequest, ResumeResponse, UpdateRequestDto,ResumeResponseDto
from app.services.api_service import process_repository
from concurrent.futures import ProcessPoolExecutor
import asyncio
import json
import logging
from app.services.stack_service import generate_techstack
from app.services.gpt_service import generate_aboutme, resume_update
from app.services.data_service import find_field_for_text, update_field_by_path, get_value_by_path
from app.config.settings import settings
from copy import deepcopy
from pydantic import ValidationError

router = APIRouter()


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

        print(updated_resume)
        # return updated_resume

        # 업데이트된 결과 확인
        print("=== Updated Resume Data ===")
        if hasattr(updated_resume, "dict"):
            updated_resume_dict = updated_resume.dict()
        else:
            updated_resume_dict = updated_resume
            
        print("=== Updated Resume 딕트 ===") 
        print(updated_resume_dict)
        print(json.dumps(updated_resume_dict, indent=4, ensure_ascii=False))

        # 선택된 텍스트가 어느 필드에 있는지 찾기
        print("=== 선택된 텍스트의 필드 찾기 ===")
        matching_fields = find_field_for_text(request.resumeInfo.dict(), request.selectedText)
        print(f"🔍 매칭된 필드 경로: {matching_fields}")

        if not matching_fields:
            raise HTTPException(status_code=400, detail="Selected text does not match any field in the context data.")

        
        # 원본 데이터를 deepcopy
        original_data = deepcopy(request.resumeInfo.dict())
        
        print(original_data)
        # return updated_resume
        # 수정된 필드만 병합
        for field_path in matching_fields:
            updated_value = get_value_by_path(updated_resume_dict, field_path)
            print(f"✅ 수정된 값 for path {field_path}: {updated_value}")
            if updated_value is not None:
                update_field_by_path(original_data, field_path, updated_value)

        # 병합 후 데이터 확인
        print("=== 병합된 최종 데이터 확인 ===")
        print(json.dumps(original_data, indent=4, ensure_ascii=False))

        # DTO 변환
        updated_response = ResumeResponseDto(**original_data)
        print("=== DTO 변환 성공 ===")
        return updated_response

    except ValidationError as e:
        print(f"❌ DTO Validation Error: {e.json()}")
        raise HTTPException(status_code=422, detail=f"DTO validation failed: {e.json()}")

    except Exception as e:
        print(f"❌ Error in update_resume: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while updating the resume.")
    
# 이력서 생성 api
@router.post("/api/ai/resumes", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    logging.basicConfig(level=logging.INFO)

    # 각 레포지토리 요약을 멀티프로세싱으로 처리
    with ProcessPoolExecutor() as executor:
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(executor, process_repository, request.template, repo_url, request.githubID, request.githubName, request.requirements)
            for repo_url in request.selectedRepo
        ]
        try:
            # 실패 시 예외를 발생시키고 에러 메시지를 리턴
            project_data = await asyncio.gather(*tasks)

        except Exception as e:
            logging.error(f"Error processing repositories: {e}")
            return {"error": f"Error processing repositories: {str(e)}"}
    
    # 레포 이름
    repo_name = "/".join(str(request.selectedRepo[0]).rstrip('/').split('/')[-2:])
        
    # 공동생성 부분
    techStack = generate_techstack(settings.gh_token, repo_name)
    aboutMe = generate_aboutme(settings.openai_api_key)
    
    resume_response = ResumeResponse(
        template=request.template,
        techStack=techStack,
        aboutMe=aboutMe,
        projects=project_data
    )
    print(resume_response)
    
    return resume_response