from typing import Literal

def calculate_mac(pattern: list[float], filter_arr: list[list[float]]) -> float:
    # 이중 반복문을 이용한 MAC연산
    score = 0.0
    for i in range(len(pattern)):
        for j in range(len(pattern[0])):
            score += float(pattern[i][j]) * float(filter_arr[i][j])
    
    return score

def compare_scores(score_a: float, score_b: float, epsilon: float = 1e-9):
    # 부동소수점 오차를 고려한 점수 비교 정책
    if abs(score_a - score_b) < epsilon:
        return "UNDECIDED"
    return "A" if score_a > score_b else "B"

def get_standard_decision(
    winner_label: Literal["UNDECIDED", "A", "B"], 
    score_a: float, 
    score_b: float
) -> Literal["Cross", "X", "UNDECIDED"]:
    # 필터 종류에 따른 최종 라벨 결정 (A: Cross, B: X 대응 가정)
    if winner_label == "UNDECIDED":
        return "UNDECIDED"
    return "Cross" if winner_label == "A" else "X"