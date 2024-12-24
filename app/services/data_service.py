import os
import json
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
  
# 수정된 내용의 value 찾기      
def find_field_for_text(context_data: dict, selected_text: str) -> list:
    matching_fields = []

    def search_field(data, path=""):
        if isinstance(data, dict):
            for key, value in data.items():
                # print(f"딕셔너리 탐색 중: 현재 키 = {key}, 현재 경로 = {path}")
                search_field(value, f"{path}.{key}" if path else key)
        elif isinstance(data, list):
            for idx, item in enumerate(data):
                # print(f"리스트 탐색 중: 현재 인덱스 = {idx}, 현재 경로 = {path}")
                search_field(item, f"{path}[{idx}]")
        else:
            # print(f"Checking value: {data} at Path: {path}")
            if isinstance(data, str) and selected_text in data:
                print(f"선택된 텍스트 포함: 경로 = {path}")
                matching_fields.append(path)

    search_field(context_data)
    print(f"최종 매칭된 경로: {matching_fields}")
    return matching_fields

# 경로에 해당하는 필드 업데이트
def update_field_by_path(original_data: dict, path: str, updated_value):
    print(f"필드 업데이트 시작: 경로 = {path}, 새 값 = {updated_value}")

    # updated_value가 Pydantic 객체인 경우 직렬화
    if hasattr(updated_value, 'dict'):
        updated_value = updated_value.dict()
    elif hasattr(updated_value, 'json'):
        updated_value = json.loads(updated_value.json())

    keys = path.replace("[", ".").replace("]", "").split(".")
    current = original_data
    

    for key in keys[:-1]:
        if key.isdigit():  # 리스트 인덱스 처리
            current = current[int(key)]
        else:
            current = current[key]

    last_key = keys[-1]
    print(f"최종 업데이트할 키: {last_key}")
    if last_key.isdigit():
        current[int(last_key)] = updated_value
    else:
        current[last_key] = updated_value
        
    print(f"업데이트 완료! 최종 데이터:\n{json.dumps(original_data, indent=4, ensure_ascii=False)}")

def get_value_by_path(data: dict, path: str):
    """
    경로(path)를 따라 데이터에서 값을 가져옵니다.
    """
    keys = path.replace("[", ".").replace("]", "").split(".")
    current = data

    for key in keys:
        if isinstance(current, list) and key.isdigit():
            current = current[int(key)]
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return None  # 경로가 잘못된 경우 None 반환
    return current