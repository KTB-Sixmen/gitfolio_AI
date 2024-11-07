from app.config.settings import settings
from github import Github
from git import Repo
import zipfile
import io
import os
import shutil
import requests

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
def download_and_extract_zip(gh_token, githubID, repo_url):
    try:
        # GitHub API로 리포지토리 가져오기
        g = Github(gh_token)
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

# PR을 가져와서 문자열로 결합하는 함수 - github api요청
def get_combined_pr_text(gh_token, githubID, repo_url):
    try:
        # GitHub API로 리포지토리 가져오기
        g = Github(gh_token)
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

# 사용자가 개발 도중에 이름이나, 닉네임을 변경하게되면 두개의 이름을 어떻게 기억하지?
# 사용자가 작성한 모든 커밋의 diff 가져와서 문자열로 결합하는 함수
def get_combined_commit_diffs(gh_token, githubID, githubName, repo_url, clone_dir=settings.repo_directory):
    """
    주어진 리포지토리에서 사용자가 작성한 커밋의 diff를 모두 가져와 하나의 문자열로 결합하는 함수
    """
    try:
        # # GitHub API로 리포지토리 가져오기
        # g = Github(gh_token)
        # repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        # repo = g.get_repo(repo_name) # 레포 추출

        # commits = repo.get_commits(author=githubID)  # 사용자가 작성한 모든 커밋 가져오기
        # combined_diff_text = ""

        # for commit in commits:
        #     commit_data = repo.get_commit(commit.sha)
        #     if commit_data.author.login == githubID:  # 커밋 작성자 확인
        #         diff = commit_data.files  # 커밋의 diff 가져오기
        #         for file in diff:
                    
        #             file_diff = file.patch if file.patch else "(No diff provided)"
        #             combined_diff_text += f"Commit: {commit.commit.message}\nFile: {file.filename}\nDiff:\n{file_diff}\n\n" + "="*50 + "\n\n"
        
        # Clone data 활용
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        repo_path = os.path.join(clone_dir, repo_name.replace("/", "_"))

        repo = Repo(repo_path)
        combined_diff_text = ""

        commits = list(repo.iter_commits())
        first_commit = commits[-1]  # 가장 처음 커밋

        # 커밋 작성자 확인을 위한 기준 설정
        author_name = githubName if githubName else githubID
        
        for commit in commits:
            # 커밋 작성자 확인
            if commit.author.name == author_name:
                commit_message = commit.message.strip()
                combined_diff_text += f"Commit: {commit_message}\n{'='*50}\n"

                # 처음 커밋: 보통 레포생성할때 중요한 정보없이 커밋함.
                if commit == first_commit:
                    pass

                # 이후 커밋: 변경된 라인만 표시
                else:
                    for diff in commit.diff(commit.parents[0], create_patch=True):
                        if diff.b_path and any(diff.b_path.endswith(ext) for ext in FILE_EXTENSIONS):
                            file_diff_text = f"File: {diff.b_path}\n"
                            
                            # 각 파일에서 변경된 라인의 줄 번호와 변경 내용 추출
                            diff_lines = diff.diff.decode('utf-8', errors='ignore').splitlines()
                            for line in diff_lines:
                                if line.startswith('@@'):
                                    file_diff_text += f"{line}\n"  # 수정된 라인정보
                                elif line.startswith('+') and not line.startswith('+++'):
                                    file_diff_text += f"Added Line: {line}\n"
                                elif line.startswith('-') and not line.startswith('---'):
                                    file_diff_text += f"Removed Line: {line}\n"

                            combined_diff_text += file_diff_text + "\n" + "="*50 + "\n\n"

        if not combined_diff_text:
            print(f"No commit diffs found for owner {githubID}.")
        else:
            print(f"All commit diffs with line information combined into a single string.")
        
        return combined_diff_text

    except Exception as e:
        print(f"Error while fetching and combining commit diffs with line information: {e}")
        return ""  # 오류 발생 시 빈 문자열 반환
    
# 주어진 리포지토리에서 가장 최근 커밋과 가장 처음 커밋의 날짜를 'yyyy.mm' 형식의 문자열로 반환하는 함수
def get_commit_dates(gh_token, repo_url):
    try:
        # GitHub API로 리포지토리 가져오기
        g = Github(gh_token)
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

# GitHub 리포지토리를 클론 한 뒤, 특정 파일을 추출하는 함수
def clone_and_extract_files(repo_url, clone_dir=settings.repo_directory):
    try:
        # 디렉토리가 없으면 생성
        if not os.path.exists(clone_dir):
            os.makedirs(clone_dir)
        
        # GitHub 리포지토리를 클론 (토큰 없이 일반 URL 사용)
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        clone_url = f"https://github.com/{repo_name}.git"
        repo_path = os.path.join(clone_dir, repo_name.replace("/", "_"))  # 저장할 디렉토리

        # 이미 클론된 경우 다시 클론하지 않음
        if not os.path.exists(repo_path):
            print(f"Cloning repository {repo_name} into {repo_path}")
            Repo.clone_from(clone_url, repo_path)
        else:
            print(f"Repository {repo_name} already cloned at {repo_path}")
        
        # 파일 내용을 읽고 필터링하여 특정 확장자의 파일만 결합
        all_code = ""
        for root, _, files in os.walk(repo_path):
            for file in files:
                if any(file.endswith(ext) for ext in FILE_EXTENSIONS):
                    file_path = os.path.join(root, file)
                    print(f"Processing file: {file_path}")
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        all_code += f.read() + "\n"

        return all_code

    except Exception as e:
        print(f"Error while cloning or processing files: {e}")
        return ""

# repo_url을 사용하여 생성된 폴더를 삭제하는 함수
def delete_cloned_repo_from_url(repo_url, clone_dir=settings.repo_directory):
    try:
        # repo_url에서 리포지토리 이름 추출
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        repo_path = os.path.join(clone_dir, repo_name.replace("/", "_"))  # 저장된 디렉토리 경로
        
        # 디렉토리가 존재하는지 확인하고 삭제
        if os.path.exists(repo_path):
            shutil.rmtree(repo_path)
            print(f"Deleted folder: {repo_path}")
        else:
            print(f"Folder does not exist: {repo_path}")
    except Exception as e:
        print(f"Error deleting folder {repo_path}: {e}")
