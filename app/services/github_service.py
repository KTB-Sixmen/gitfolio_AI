from github import Github
import zipfile
import io
import requests
from typing import List, Tuple

FILE_EXTENSIONS = ['.py', '.js', '.java', '.cpp', '.c', '.go', '.rb', '.ts', '.html', '.md' ]

# GitHub 리포지토리의 디폴트 브랜치를 가져오는 기능
def get_default_branch(repo):
    try:
        default_branch = repo.default_branch  # 디폴트 브랜치 가져오기
        print(f"Default branch: {default_branch}")
        return default_branch
    except Exception as e:
        print(f"Error fetching default branch: {e}")
        return None  # 오류 발생 시 None 반환
    
# GitHub 리포지토리의 ZIP 파일을 메모리에 다운로드 및 압축 해제
def download_and_extract_zip(github_token, githubID, repo_url):
    try:
        # GitHub API로 리포지토리 가져오기
        g = Github(github_token)
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        repo = g.get_repo(repo_name) # 레포 추출

        # 디폴트 브랜치 가져오기
        default_branch = get_default_branch(repo) 

        url = f"https://github.com/{repo_name}/archive/refs/heads/{default_branch}.zip"
        response = requests.get(url)
        if response.status_code == 200:
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            return zip_file
        else:
            print(f"Failed to download repository ZIP file: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error downloading ZIP file: {e}")
        return None

# ZIP 파일에서 특정 확장자 파일만 가져와 모든 코드를 하나의 문자열로 결합
def get_code_files_from_zip(zip_file):
    try:
        if not zip_file:
            return ""
        all_code = ""
        for file_info in zip_file.infolist():
            if any(file_info.filename.endswith(ext) for ext in FILE_EXTENSIONS):
                print(f"Processing file: {file_info.filename}")
                with zip_file.open(file_info) as file:
                    file_content = file.read().decode('utf-8', errors='ignore')
                    all_code += file_content + "\n"
        return all_code
    except Exception as e:
        print(f"Error extracting files from ZIP: {e}")
        return ""

# PR을 가져와서 문자열로 결합하는 함수
def get_combined_pr_text(github_token, githubID, repo_url):
    try:
        # GitHub API로 리포지토리 가져오기
        g = Github(github_token)
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        repo = g.get_repo(repo_name) # 레포 추출

        pull_requests = repo.get_pulls(state='closed')  # 닫힌 PR만 가져오기
        combined_text = ""

        for pr in pull_requests:
            if pr.user.login == githubID:  # 소유자가 작성한 PR인지 확인
                title = pr.title
                body = pr.body if pr.body else "(No PR description provided)"
                combined_text += f"Title: {title}\n\nDescription: {body}\n\n" + "="*50 + "\n\n"

        if not combined_text:
            print(f"No pull requests found for owner {githubID}.")
        else:
            print(f"All PRs combined into a single string.")
        
        return combined_text

    except Exception as e:
        print(f"Error while fetching and combining pull requests: {e}")
        return ""  # 오류 발생 시 빈 문자열 반환

# 사용자가 작성한 모든 커밋의 diff 가져와서 문자열로 결합하는 함수
def get_combined_commit_diffs(github_token, githubID, repo_url):
    """
    주어진 리포지토리에서 사용자가 작성한 커밋의 diff를 모두 가져와 하나의 문자열로 결합하는 함수
    """
    try:
        # GitHub API로 리포지토리 가져오기
        g = Github(github_token)
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        repo = g.get_repo(repo_name) # 레포 추출

        commits = repo.get_commits(author=githubID)  # 사용자가 작성한 모든 커밋 가져오기
        combined_diff_text = ""

        for commit in commits:
            commit_data = repo.get_commit(commit.sha)
            if commit_data.author.login == githubID:  # 커밋 작성자 확인
                diff = commit_data.files  # 커밋의 diff 가져오기
                for file in diff:
                    file_diff = file.patch if file.patch else "(No diff provided)"
                    combined_diff_text += f"Commit: {commit.commit.message}\nFile: {file.filename}\nDiff:\n{file_diff}\n\n" + "="*50 + "\n\n"

        if not combined_diff_text:
            print(f"No commit diffs found for owner {githubID}.")
        else:
            print(f"All commit diffs combined into a single string.")
        
        return combined_diff_text

    except Exception as e:
        print(f"Error while fetching and combining commit diffs: {e}")
        return ""  # 오류 발생 시 빈 문자열 반환
    
    
# 주어진 리포지토리에서 가장 최근 커밋과 가장 처음 커밋의 날짜를 'yyyy.mm' 형식의 문자열로 반환하는 함수
def get_commit_dates(github_token, repo_url):
    try:
        # GitHub API로 리포지토리 가져오기
        g = Github(github_token)
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        repo = g.get_repo(repo_name)  # 레포지토리 추출

        # 모든 커밋 리스트 가져오기 (처음 커밋부터 최근 커밋 순서로 정렬)
        commits = list(repo.get_commits())
        
        if not commits:
            print(f"No commits found in repository {repo_name}.")
            return None, None
        
        # 가장 처음 커밋과 가장 최근 커밋 추출
        first_commit = commits[-1]  # 가장 오래된 커밋 (목록의 끝)
        latest_commit = commits[0]  # 가장 최근 커밋 (목록의 시작)

        # 날짜를 'yyyy.mm' 형식의 문자열로 변환
        first_commit_date = first_commit.commit.author.date.strftime('%Y.%m')
        latest_commit_date = latest_commit.commit.author.date.strftime('%Y.%m')

        return first_commit_date, latest_commit_date

    except Exception as e:
        print(f"Error while fetching commit dates: {e}")
        return None, None