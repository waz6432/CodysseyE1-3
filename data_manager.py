import json

def normalize_label(label):
    # 입력된 라벨을 내부 표준(Cross, X)으로 변환
    mapping = {
        '+': 'Cross', 'cross': 'Cross', 'Cross': 'Cross',
        'x': 'X', 'X': 'X'
    }
    return mapping.get(label, label)

def get_user_input_3x3(prompt_name):
    # 모드 1용: 3x3 행렬 입력 및 검증
    while True:
        print(f"\n[{prompt_name}] 3x3 데이터를 한 줄씩(3개 숫자, 공백 구분) 입력하세요.")
        matrix = []
        try:
            for i in range(3):
                row = list(map(float, input(f"{i+1}행: ").split()))
                if len(row) != 3:
                    raise ValueError("열 개수가 맞지 않습니다.")
                matrix.append(row)
            return matrix
        except ValueError as e:
            print(f"⚠️ 입력 형식 오류: {e} 다시 입력해주세요.")

def load_data_json(file_path):
    # SON 로드 및 기본 구조 반환
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ {file_path} 파일을 찾을 수 없습니다.")
        return None