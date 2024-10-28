from fastapi import APIRouter
from app.dto.resume_dto import ResumeRequest, ResumeResponse, Project
from app.services.github_service import download_and_extract_zip, get_code_files_from_zip
from app.services.gpt_service import  slice_and_summarize, final_summarization
from app.config.settings import settings
from app.prompts.resume_prompt import CODE_SUMMARY_PROMPT, PR_SUMMARY_PROMPT, COMMIT_DIFF_SUMMARY_PROMPT, FINAL_SUMMARY_PROMPT, FINAL_PROJECT_PROMPT

router = APIRouter()

# # 현재 램에 다운 받는형식이라 process_repository호출하고 거기서 다 진행되고 있음
# # 이력서 생성 api
# @router.post("/api/resumes", response_model=ResumeResponse)
# async def generate_resume(request: ResumeRequest):
#     # 요청 데이터를 출력
#     print(f"GitHub ID: {request.githubID}")
#     print(f"Personal Repo: {request.personalRepo}")
#     print(f"Selected Repos: {request.selectedRepo}")
#     print(f"Requirements: {request.requirements}")

#     # 더미 데이터로 응답
#     dummy_data = {
#         "projects": [
#             {
#                 "projectName": "DREAM, 생성형AI 스토리",
#                 "projectStartedAt": "2024-09",
#                 "projectEndedAt": "2024-09",
#                 "skillSet": "RAG, Langchain, GPT4, DALL.E",
#                 "projectDescription": "<p><strong>메시징 시스템 통계 조회 API 성능 개선 (4.75s -> 41ms)</strong></p><p>의사의 회진 일정을 환자에게 메시지로 전송하는 시스템의 통계 서비스 API의 성능을 개선했습니다.</p><p>한 달간의 통계를 조회할 때 약 5초가 소요되던 API의 병목 지점을 찾아내고 수정하여 50ms 이하의 속도로 개선했습니다.</p>",
#                 "repoLink": "https://github.com/ilmin/gen-ai-dream"
#             },
#             {
#                 "projectName": "추천 시스템 개발",
#                 "projectStartedAt": "2024-07",
#                 "projectEndedAt": "2024-08",
#                 "skillSet": "KcELENTRA, BiLSTM, HDBSCAN",
#                 "projectDescription": "<p><strong>식당 리뷰 기반 추천 시스템 개발</strong></p><p>HDBSCAN과 ONNX를 활용하여 리뷰 데이터를 기반으로 한 식당 추천 시스템을 구축했습니다.</p><p>KcELECTRA와 BiLSTM 앙상블 모델을 통해 응답 속도를 222초에서 26초로 개선했습니다.</p>",
#                 "repoLink": "https://github.com/ilmin/recommendation-system"
#             }
#         ],
#         "techStack": ["Kotlin", "Java", "Python", "ONNX"],
#         "aboutMe": "안녕하세요! ’Comfort-Zone에서 벗어나 끊임없이 도전을 하는 개발자’ 조일민입니다.\n- Self-Motivation: 어떤 일이든 관심이 생기면 망설임 없이 도전하여 실행에 옮깁니다.\n- Optimization-Driven: 코드 한 줄까지도 성능 최적화에 집중하여 시스템의 효율성과 비즈니스 가치를 극대화합니다.\n- Collaborative Growth: 개인적인 성장을 넘어서, 함께 공유하며 발전하는 문화를 추구합니다."
#     }

#     return dummy_data

# 이력서 생성 api (ram->disk / 멀티프로세싱처리 각각 파트별로)
@router.post("/api/resumes", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    project_summaries = []

    # 선택된 각 레포지토리 처리
    for repo_url in request.selectedRepo:

        # 레포지토리 다운로드 및 집파일 반환
        zip_file = download_and_extract_zip(settings.github_token, request.githubID, repo_url)

        # ZIP 파일에서 특정 확장자 파일만 가져와 하나의 코드 스트링으로 결합
        all_code = get_code_files_from_zip(zip_file,)

        # 코드 내용을 슬라이싱하여 요약 진행
        initial_summary = slice_and_summarize(all_code, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=CODE_SUMMARY_PROMPT)
        
        # 최종 요약: 길이가 긴 경우 계속해서 줄여나감
        final_code_summary = final_summarization(initial_summary, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=FINAL_SUMMARY_PROMPT)

        # 3. 각 레포지토리 요약을 Project 형식에 맞게 변환
        project_summary = Project(
            projectName="ilmin_test",
            projectStartedAt="2024-07",  # 예시 데이터로 설정 (실제 데이터로 대체 가능)
            projectEndedAt="2024-08",    # 예시 데이터로 설정
            skillSet="Python, OpenAI GPT",
            projectDescription=final_code_summary,
            repoLink=repo_url
        )
        project_summaries.append(project_summary)
    
    # 최종 이력서 응답 생성
    resume_response = ResumeResponse(
        projects=project_summaries,
        techStack=["Python", "OpenAI GPT", "FastAPI"],  # 예시 데이터
        aboutMe="안녕하세요! ‘Comfort-Zone에서 벗어나 끊임없이 도전을 하는 개발자’ 조일민입니다."
    )
    
    return resume_response