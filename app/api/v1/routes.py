from fastapi import APIRouter
from app.dto.resume_dto import ResumeRequest, ResumeResponse, Project
from app.services.github_service import download_and_extract_zip, get_code_files_from_zip, get_combined_pr_text, get_combined_commit_diffs
from app.services.gpt_service import  slice_and_summarize, final_summarization
from app.config.settings import settings
from app.prompts.resume_prompt import CODE_SUMMARY_PROMPT, PR_SUMMARY_PROMPT, COMMIT_DIFF_SUMMARY_PROMPT, FINAL_SUMMARY_PROMPT, FINAL_PROJECT_PROMPT

router = APIRouter()

# 이력서 생성 api (ram->disk / 멀티프로세싱처리 각각 파트별로)
@router.post("/api/resumes", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    project_summaries = []

    # 선택된 각 레포지토리 처리
    for repo_url in request.selectedRepo:

        # 1. ALL CODE
        # 레포지토리 다운로드 및 집파일 반환
        zip_file = download_and_extract_zip(settings.github_token, request.githubID, repo_url)

        # ZIP 파일에서 특정 확장자 파일들만 가져와 하나의 코드 문자열로 결합
        all_code = get_code_files_from_zip(zip_file,)

        # 코드 내용을 슬라이싱하여 요약 진행
        initial_summary = slice_and_summarize(all_code, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=CODE_SUMMARY_PROMPT)
        
        # 최종 요약: 길이가 긴 경우 계속해서 줄여나감
        final_code_summary = final_summarization(initial_summary, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=FINAL_SUMMARY_PROMPT)

        # 2. PR
        # 소유자가 작성한 PR을 가져와서 하나의 큰 문자열로 결합
        combined_pr_text = get_combined_pr_text(settings.github_token, request.githubID, repo_url)

        # 결합된 PR 내용을 요약
        initial_pr_summary = slice_and_summarize(combined_pr_text, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=PR_SUMMARY_PROMPT)
        
        # 최종 요약: 길이가 긴 경우 계속해서 줄여나감
        final_pr_summary = final_summarization(initial_pr_summary, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=FINAL_SUMMARY_PROMPT)

        # 3. Commits
        # 소유자가 작성한 커밋 diff를 가져와서 하나의 큰 문자열로 결합
        combined_commit_diffs = get_combined_commit_diffs(settings.github_token, request.githubID, repo_url)

        # 결합된 커밋 diff 내용을 요약
        initial_commit_summary = slice_and_summarize(combined_commit_diffs, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=COMMIT_DIFF_SUMMARY_PROMPT)

        # 최종 요약: 길이가 긴 경우 계속해서 줄여나감
        final_commit_summary = final_summarization(initial_commit_summary, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=FINAL_SUMMARY_PROMPT)

        print(final_code_summary)
        print("\n-------------------\n")
        print(final_pr_summary)
        print("\n-------------------\n")
        print(final_commit_summary)
        print("\n-------------------\n")

        # 각 레포지토리 요약을 Project 형식에 맞게 변환
        project_summary = Project(
            projectName="ilmin_test",
            projectStartedAt="2024-07", 
            projectEndedAt="2024-08",  
            skillSet="Python, OpenAI GPT",
            projectDescription=final_code_summary,
            repoLink=repo_url
        )
        project_summaries.append(project_summary)
    
    # 최종 이력서 응답 생성
    resume_response = ResumeResponse(
        projects=project_summaries,
        techStack=["Python", "OpenAI GPT", "FastAPI"], 
        aboutMe="안녕하세요! ‘Comfort-Zone에서 벗어나 끊임없이 도전을 하는 개발자’ 조일민입니다."
    )
    
    return resume_response