import os
from app.config.settings import settings

# 폴더 경로 생성 함수
def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path, exist_ok=True)  # 모든 하위 디렉토리를 포함해 생성

# 요약된 코드 결과 저장 함수
def save_summaries_to_file(summary, githubID, repo_url, output_folder=settings.default_data):
    try:
        if not summary.strip():  # 내용이 없으면 파일 저장 스킵
            print("No summary to save. Skipping file save.")
            return
        
        repo_name = "/".join(str(repo_url).rstrip('/').split('/')[-2:])
        # repo_fullname에서 마지막 부분만 사용
        repo = repo_name.split('/')[-1]
        
        # owner와 repo를 언더스코어로 결합
        folder_name = f"{githubID}_{repo}.txt"
        
        # 폴더 경로가 없으면 생성
        create_folder_if_not_exists(output_folder)
        
        output_file = os.path.join(output_folder, folder_name)

        print(f"Saving code summary to file: {output_file}")
        with open(output_file, 'w') as f:
            f.write(f"Summary:\n{summary}\n")
            f.write("="*50 + "\n")
    except Exception as e:
        print(f"Error saving code summary to file: {e}")