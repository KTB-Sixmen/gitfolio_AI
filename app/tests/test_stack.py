import os
import json
from dotenv import load_dotenv

import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from app.services.stack_service import generate_techstack 

print(os.getcwd())

def test_generate_techstack():
    # 1. .env 파일에서 환경 변수 로드
    load_dotenv()  # .env 파일의 내용 로드
    github_token = os.getenv("GH_TOKEN")  # GitHub 토큰 가져오기
    if not github_token:
        raise ValueError("GitHub Token이 .env 파일에 설정되지 않았습니다.")

    # 2. 테스트 데이터 준비
    project_summaries = [
        {
            "projectName": "Project Alpha",
            "skillSet": "Python, Flask, Docker",
            "projectDescription": "A backend project using Flask for API development and Docker for containerization."
        },
        {
            "projectName": "Project Beta",
            "skillSet": "JavaScript, React, Node.js",
            "projectDescription": "A full-stack project using React for frontend and Node.js for backend."
        }
    ]
    repo_name = "Oh-JunTaek/gitportfolio"  # 테스트할 레포지토리 이름

    # 3. 함수 호출
    try:
        tech_stack = generate_techstack(project_summaries, github_token, repo_name)
        print("Generated Tech Stack:")
        print(tech_stack)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    test_generate_techstack()
