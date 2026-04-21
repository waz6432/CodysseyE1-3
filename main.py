import sys
from mac_logic import calculate_mac, compare_scores, get_standard_decision
from data_manager import normalize_label, get_user_input_3x3, load_data_json
from evaluator import measure_average_time

def run_mode_1():
    print("\n--- [모드 1] 사용자 입력 (3x3) ---")
    filter_a = get_user_input_3x3("필터 A (Cross)")
    filter_b = get_user_input_3x3("필터 B (X)")
    pattern = get_user_input_3x3("패턴")

    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)
    
    winner = compare_scores(score_a, score_b)
    avg_time = measure_average_time(pattern, filter_a)

    final_display = winner if winner != "UNDECIDED" else "판정 불가"

    print("\n[결과 화면]")
    print(f"- MAC 점수: A={score_a:.4f}")
    print(f"- MAC 점수: B={score_b:.4f}")
    print(f"- 연산 시간(평균/10회)): {avg_time:.6f} ms")
    print(f"- 최종 판정: {final_display}")

def run_mode_2():
    data = load_data_json('data.json')
    if not data: return

    filters = data.get('filters', {})
    patterns = data.get('patterns', {})
    
    results = []
    performance_data = []

    print("\n--- [모드 2] JSON 데이터 분석 ---")
    for key, item in patterns.items():
        try:
            # 키에서 사이즈 추출 (예: size_5_1 -> size_5)
            size_key = f"size_{key.split('_')[1]}"
            pattern_data = item['input']
            expected = normalize_label(item['expected'])
            
            # 필터 선택 (해당 사이즈의 cross와 x 필터)
            f_cross = filters[size_key]['cross']
            f_x = filters[size_key]['x']

            # 크기 검증
            if len(pattern_data) != len(f_cross):
                results.append({'id': key, 'result': 'FAIL', 'reason': 'Size Mismatch'})
                continue

            # 연산
            s_cross = calculate_mac(pattern_data, f_cross)
            s_x = calculate_mac(pattern_data, f_x)
            
            winner_node = compare_scores(s_cross, s_x)
            actual = get_standard_decision(winner_node, s_cross, s_x)
            
            status = "PASS" if actual == expected else "FAIL"
            results.append({'id': key, 'result': status, 'actual': actual, 'expected': expected})
            
            # 성능 데이터 저장 (사이즈별)
            performance_data.append({'size': len(pattern_data), 'time': measure_average_time(pattern_data, f_cross)})

        except Exception as e:
            results.append({'id': key, 'result': 'FAIL', 'reason': str(e)})

    # 결과 요약 출력
    total = len(results)
    pass_cnt = sum(1 for r in results if r['result'] == 'PASS')
    print(f"\n[전체 리포트] 총계: {total} | 통과: {pass_cnt} | 실패: {total - pass_cnt}")
    
    if total - pass_cnt > 0:
        print("- 실패 케이스 목록:")
        for r in results:
            if r['result'] == 'FAIL':
                print(f"  * {r['id']}: {r.get('reason', 'Label Mismatch')}")

def main():
    while True:
        print("\n==== MAC Pattern Matcher ====")
        print("1. 사용자 입력 분석 (3x3)")
        print("2. JSON 데이터 분석 (data.json)")
        print("0. 종료")
        choice = input("선택: ")
        
        if choice == '1': run_mode_1()
        elif choice == '2': run_mode_2()
        elif choice == '0': break
        else: print("잘못된 입력입니다.")

if __name__ == "__main__":
    main()