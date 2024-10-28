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

        repo = g.get_repo("KakaoTechBC-GOATNINE/kakao_mlms_AI") # 소유자와 레포이름만 추출
        # 디폴트 브랜치 가져오기
        default_branch = get_default_branch(repo) 

        url = f"https://github.com/KakaoTechBC-GOATNINE/kakao_mlms_AI/archive/refs/heads/{default_branch}.zip"
        print(url)
        response = requests.get(url)
        if response.status_code == 200:
            zip_file = zipfile.ZipFile(io.BytesIO(response.content))
            print("woring3")
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