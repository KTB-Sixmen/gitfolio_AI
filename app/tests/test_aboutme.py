import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(project_root)

from app.services.gpt_service import generate_aboutme
from app.config.settings import settings

# 유저 입력 값 설정
def mock_github_profile_and_repos():
    """
    Mocking GitHub Profile and Repos data
    """
    print("Please enter your GitHub README content:")
    github_readme = input("> ")

    print("Please enter your GitHub repositories information:")
    print("Example format: Repo1: Description1\nRepo2: Description2")
    github_repos = input("> ")

    return github_readme, github_repos

# OpenAI API 키 (실제 값이 필요할 경우 설정)
openai_api_key = settings.openai_api_key

# Mock GitHub 데이터를 입력받음
github_readme, github_repos = mock_github_profile_and_repos()

# 테스트 함수 실행
result = generate_aboutme(openai_api_key=openai_api_key, prompt=settings.aboutme_prompt)

# 결과 출력
print("\nGenerated 'About Me':")
print(result)