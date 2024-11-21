import os
import json
from github import Github

def generate_techstack(github_token, repo_name):
    # GitHub 인증 및 레포지토리 접근
    g = Github(github_token)
    repo = g.get_repo(repo_name)
    
    # 프로젝트 루트 경로 설정
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 현재 파일 기준 상위 폴더
    dependency_folder = os.path.join(BASE_DIR, "data", "dependencies")

    # 파일 경로 정의
    dependency_file_path = os.path.join(dependency_folder, "dependency.json")
    frameworks_file_path = os.path.join(dependency_folder, "frameworks.json")

    # 파일 읽기
    with open(dependency_file_path, "r") as f:
        dependency_files = json.load(f)

    with open(frameworks_file_path, "r") as f:
        frameworks_data = json.load(f)

    # 종속성 파일에서 추출한 라이브러리와 기술 스택
    used_frameworks = set()
    all_dependency_files = [file for files in dependency_files.values() for file in files]

    # GitHub 레포지토리에서 언어 분석
    languages = repo.get_languages()
    print(languages)

    # 종속성 파일 분석 및 기술 매칭
    contents = repo.get_contents("")
    
    print(contents)
    for content_file in contents:
        print(content_file.name)
        if content_file.name in all_dependency_files:
            file_content = repo.get_contents(content_file.path).decoded_content.decode()
            for lang in languages.keys():
                if lang in frameworks_data:
                    for framework in frameworks_data[lang]:
                        if framework.lower() in file_content.lower():
                            used_frameworks.add(framework)

    # # 프로젝트 요약에서 스킬셋 추출 (딕셔너리 접근 방식)
    # skillsets = [
    #     skill.strip()
    #     for project in project_summaries
    #     for skill in project["skillSet"].split(",")
    # ]
    
        # 토픽에서 프레임워크 추출
    topics = repo.get_topics()
    print("Topics:", topics)
    for topic in topics:
        for lang in languages.keys():
            if lang in frameworks_data:  # 언어와 연결된 프레임워크만 확인
                for framework in frameworks_data[lang]:
                    if framework.lower() in topic.lower():
                        print(f"Framework matched from topic '{topic}': {framework}")
                        used_frameworks.add(framework)
                        
                        
    
    used_frameworks.update(languages.keys())

    print(used_frameworks)

    # 기술 스택 결과 정리
    tech_stack = sorted(used_frameworks)
    return tech_stack
