from fastapi import APIRouter
from app.dto.resume_dto import ResumeRequest, ResumeResponse, Project
from app.services.github_service import download_and_extract_zip, get_code_files_from_zip, get_combined_pr_text, get_combined_commit_diffs, get_commit_dates, clone_and_extract_files, delete_cloned_repo_from_url
from app.services.gpt_service import  slice_and_summarize, final_summarization, generate_project_summary, simplify_project_summary_byJson
from app.services.data_service import save_summaries_to_file
from app.config.settings import settings

router = APIRouter()

# 예외처리 할것
# 이력서 생성 api (ram->disk / 멀티프로세싱처리 각각 파트별로)
@router.post("/api/resumes", response_model=ResumeResponse)
async def generate_resume(request: ResumeRequest):
    project_summaries = []

    # 선택된 각 레포지토리 처리
    for repo_url in request.selectedRepo:

        # 1. ALL CODE

        # -> 기존 방식 
        # # 레포지토리 다운로드 및 집파일 반환
        # zip_file = download_and_extract_zip(settings.gh_token, request.githubID, repo_url)

        # # ZIP 파일에서 특정 확장자 파일들만 가져와 하나의 코드 문자열로 결합
        # all_code = get_code_files_from_zip(zip_file)

        # -> 코드 클론하는 형식으로 변경
        all_code = clone_and_extract_files(repo_url)

        # 코드 내용을 슬라이싱하여 요약 진행
        initial_summary = slice_and_summarize(all_code, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=settings.code_summary_prompt)
        
        # 최종 요약: 길이가 긴 경우 계속해서 줄여나감
        final_code_summary = final_summarization(initial_summary, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=settings.final_summary_prompt)
        
        # 요약된 전체코드 내용 파일로 저장
        save_summaries_to_file(final_code_summary, request.githubID, repo_url, output_folder=settings.code_data)

        # 2. PR
        # 소유자가 작성한 PR을 가져와서 하나의 큰 문자열로 결합
        combined_pr_text = get_combined_pr_text(settings.gh_token, request.githubID, repo_url)

        # 결합된 PR 내용을 요약
        initial_pr_summary = slice_and_summarize(combined_pr_text, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=settings.pr_summary_prompt)
        
        # 최종 요약: 길이가 긴 경우 계속해서 줄여나감
        final_pr_summary = final_summarization(initial_pr_summary, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=settings.final_summary_prompt)

        # 요약된 PR 내용을 파일로 저장
        save_summaries_to_file(final_pr_summary, request.githubID, repo_url, output_folder=settings.pr_data)

        # 3. Commits
        # 소유자가 작성한 커밋 diff를 가져와서 하나의 큰 문자열로 결합
        combined_commit_diffs = get_combined_commit_diffs(settings.gh_token, request.githubID, request.githubName, repo_url)

        # 결합된 커밋 diff 내용을 요약
        initial_commit_summary = slice_and_summarize(combined_commit_diffs, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=settings.commit_diff_summary_prompt)

        # 최종 요약: 길이가 긴 경우 계속해서 줄여나감
        final_commit_summary = final_summarization(initial_commit_summary, settings.openai_api_key, max_output_tokens=settings.max_output_tokens, prompt=settings.final_summary_prompt)

        # 요약된 커밋 diff 내용을 파일로 저장
        save_summaries_to_file(final_commit_summary, request.githubID, repo_url, output_folder=settings.commit_data)

        # 4. Project
        # 최종 프로젝트 요약 생성
        project_summary = generate_project_summary(final_code_summary, final_pr_summary, final_commit_summary, settings.openai_api_key, prompt=settings.final_project_prompt)
        
        # 프로젝트 요약 저장
        save_summaries_to_file(project_summary, request.githubID, repo_url, output_folder=settings.project_data)

        # 5. Simplifying
        # 프로젝트 간단한 형태와 json 형태로 반환하기
        simplified_summary = simplify_project_summary_byJson(project_summary, settings.openai_api_key, prompt=settings.simplify_project_prompt)

        # 프로젝트 시작 및 마지막 기간 가져오기
        first_commit_date, latest_commit_date = get_commit_dates(settings.gh_token, repo_url)

        # 클론한 레포 폴더 삭제
        delete_cloned_repo_from_url(repo_url)

        # 각 레포지토리 요약을 Project 형식에 맞게 변환
        project_summary = Project(
            projectName=simplified_summary.projectName, 
            projectStartedAt=first_commit_date, 
            projectEndedAt=latest_commit_date,  
            skillSet=simplified_summary.skillSet,
            projectDescription=simplified_summary.projectDescription,
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

