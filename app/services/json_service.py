import json

def find_key_by_value(json_data, target_value):
    """
    JSON 데이터에서 target_value를 가진 키를 재귀적으로 검색합니다.
    """
    for key, value in json_data.items():  # JSON 데이터의 각 키-값 쌍을 순회
        if isinstance(value, dict):  # 값이 중첩된 딕셔너리인 경우
            result = find_key_by_value(value, target_value)  # 재귀적으로 해당 딕셔너리 내부 탐색
            if result:
                return f"{key}.{result}"  # 부모 키와 결과 키를 합쳐 반환
        elif isinstance(value, list):  # 값이 리스트인 경우
            for i, item in enumerate(value):  # 리스트의 각 항목을 순회
                if isinstance(item, dict):  # 리스트 항목이 딕셔너리인 경우
                    result = find_key_by_value(item, target_value)  # 딕셔너리를 재귀적으로 탐색
                    if result:
                        return f"{key}[{i}].{result}"  # 부모 키와 인덱스를 포함한 경로 반환
                elif item == target_value:  # 리스트 항목이 target_value와 동일한 경우
                    return f"{key}[{i}]"  # 리스트의 인덱스를 포함한 경로 반환
        elif value == target_value:  # 값이 target_value와 동일한 경우
            return key  # 키 반환
    return None  # target_value를 찾지 못한 경우 None 반환


def update_json_by_key(json_data, key_path, new_value):
    """
    JSON 데이터에서 지정된 key_path에 있는 값을 new_value로 업데이트합니다.
    """
    keys = key_path.split('.')  # key_path를 '.' 기준으로 나눠 리스트로 변환
    current = json_data  # JSON 데이터를 탐색하기 위해 초기화

    for key in keys[:-1]:  # 마지막 키를 제외한 경로를 순회
        if '[' in key and ']' in key:  # 키가 리스트 인덱스를 포함하는 경우
            list_key, index = key[:-1].split('[')  # 리스트 키와 인덱스를 분리
            current = current[list_key][int(index)]  # 리스트 인덱스를 사용해 값 탐색
        else:  # 리스트가 아닌 일반 키인 경우
            current = current[key]  # 키를 사용해 값 탐색

    final_key = keys[-1]  # 경로의 마지막 키
    if '[' in final_key and ']' in final_key:  # 마지막 키가 리스트 인덱스를 포함하는 경우
        list_key, index = final_key[:-1].split('[')  # 리스트 키와 인덱스를 분리
        current[list_key][int(index)] = new_value  # 새로운 값으로 업데이트
    else:  # 마지막 키가 리스트 인덱스가 아닌 경우
        current[final_key] = new_value  # 새로운 값으로 업데이트