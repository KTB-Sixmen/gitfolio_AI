from app.dto.resume_dto import Project
from app.services.github_service import get_combined_pr_text, get_combined_commit_diffs, get_commit_dates, clone_and_extract_files, delete_cloned_repo_from_url
from app.services.gpt_service import  slice_and_summarize, final_summarization, generate_project_summary, generate_project_summary_byJson, simplify_project_summary_byJson
from app.services.data_service import save_summaries_to_file
from app.config.settings import settings
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# 병렬로 레포지토리를 처리하고 요약을 반환하는 함수
def process_repository(repo_url, githubID, githubName, requirements):
    try:
        with ThreadPoolExecutor() as executor:
            all_code = clone_and_extract_files(repo_url)
            # 1, 2, 3번 작업을 병렬로 실행
            futures = {
                executor.submit(process_code_files, all_code, repo_url, githubID, requirements): 'code_summary',
                executor.submit(process_pr_text, repo_url, githubID, requirements): 'pr_summary',
                executor.submit(process_commit_diffs, repo_url, githubID, githubName, requirements): 'commit_summary'
            }
            results = {}
            for future in as_completed(futures):
                key = futures[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    logging.error(f"Error in {key}: {e}")
                    raise  # 에러를 다시 발생시켜 상위에서 예외 처리

        # 병렬처리 결과 할당
        final_code_summary = results['code_summary']
        final_pr_summary = results['pr_summary']
        final_commit_summary = results['commit_summary']

        # 이후 작업들
        project_summary = create_project_summary(final_code_summary, final_pr_summary, final_commit_summary, githubID, repo_url, requirements)
        simplified_summary = simplify_project_info(project_summary, requirements)
        first_commit_date, latest_commit_date = create_repo_start_end_date(repo_url)
        delete_cloned_repo_from_url(repo_url)

        project_summary += f"\n\n### 프로젝트 요약\n {simplified_summary.projectDescription}**"

        project_summary = Project(
            projectName=simplified_summary.projectName, 
            projectStartedAt=first_commit_date, 
            projectEndedAt=latest_commit_date,  
            skillSet=simplified_summary.skillSet,
            projectDescription=project_summary,
            repoLink=repo_url
        )
        return project_summary

    except Exception as e:
        logging.error(f"Error in processing repository {repo_url}: {e}")
        raise  # 에러를 다시 발생시켜 상위에서 예외 처리

# 클론하여 코드 파일을 가져오고 요약을 생성하는 함수
def process_code_files(all_code, repo_url, githubID, requirements):
    initial_summary = slice_and_summarize(all_code, settings.openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, prompt=settings.code_summary_prompt)
    final_code_summary = final_summarization(initial_summary, settings.openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, prompt=settings.final_summary_prompt)
    save_summaries_to_file(final_code_summary, githubID, repo_url, output_folder=settings.code_data)
    return final_code_summary

# PR 텍스트를 가져와서 요약을 생성하는 함수
def process_pr_text(repo_url, githubID, requirements):
    combined_pr_text = get_combined_pr_text(settings.gh_token, githubID, repo_url)
    initial_pr_summary = slice_and_summarize(combined_pr_text, settings.openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, prompt=settings.pr_summary_prompt)
    final_pr_summary = final_summarization(initial_pr_summary, settings.openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, prompt=settings.final_summary_prompt)
    save_summaries_to_file(final_pr_summary, githubID, repo_url, output_folder=settings.pr_data)
    return final_pr_summary

# 커밋 diff 내용을 가져와서 요약을 생성하는 함수
def process_commit_diffs(repo_url, githubID, githubName, requirements):
    combined_commit_diffs = get_combined_commit_diffs(settings.gh_token, githubID, githubName, repo_url)
    initial_commit_summary = slice_and_summarize(combined_commit_diffs, settings.openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, prompt=settings.commit_diff_summary_prompt)
    final_commit_summary = final_summarization(initial_commit_summary, settings.openai_api_key, requirements, max_output_tokens=settings.max_output_tokens, prompt=settings.final_summary_prompt)
    save_summaries_to_file(final_commit_summary, githubID, repo_url, output_folder=settings.commit_data)
    return final_commit_summary

# 코드, PR, 커밋 요약을 종합하여 프로젝트 요약 생성
def create_project_summary(code_summary, pr_summary, commit_summary, githubID, repo_url, requirements):
    project_summary = generate_project_summary(code_summary, pr_summary, commit_summary, settings.openai_api_key, requirements, prompt=settings.final_project_prompt)
    save_summaries_to_file(project_summary, githubID, repo_url, output_folder=settings.project_data)
    return project_summary

# 프로젝트 요약을 간단한 형태로 변환
def simplify_project_info(project_summary, requirements):
    simplified_summary = simplify_project_summary_byJson(project_summary, settings.openai_api_key, requirements, prompt=settings.simplify_project_prompt)
    return simplified_summary

# 시작 및 마감 날짜 반환
def create_repo_start_end_date(repo_url):
    first_commit_date, latest_commit_date = get_commit_dates(settings.gh_token, repo_url)
    return first_commit_date, latest_commit_date
