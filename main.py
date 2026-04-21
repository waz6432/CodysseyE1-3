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
    
    # --- [1] 필터 로드 섹션 ---
    print("\n#" + "-"*40)
    print("# [1] 필터 로드")
    print("#" + "-"*40)
    for size in [5, 13, 25]:
        if f"size_{size}" in filters:
            print(f"✓ size_{size} 필터 로드 완료 (Cross, X)")

    # --- [2] 패턴 분석 섹션 ---
    print("\n#" + "-"*40)
    print("# [2] 패턴 분석 (라벨 정규화 적용)")
    print("#" + "-"*40)
    
    results = []
    performance_records = []

    for key, item in patterns.items():
        try:
            size_val = key.split('_')[1]
            size_key = f"size_{size_val}"
            pattern_data = item['input']
            expected = normalize_label(item['expected'])
            f_cross = filters[size_key]['cross']
            f_x = filters[size_key]['x']

            # MAC 연산 및 시간 측정
            s_cross = calculate_mac(pattern_data, f_cross)
            s_x = calculate_mac(pattern_data, f_x)
            
            winner_node = compare_scores(s_cross, s_x)
            actual = get_standard_decision(winner_node, s_cross, s_x)
            status = "PASS" if actual == expected else "FAIL"
            
            # 케이스별 상세 출력 (이미지 스타일)
            print(f"- -- {key} ---")
            print(f"Cross 점수: {s_cross}")
            print(f"X 점수: {s_x}")
            
            fail_reason = ""
            if winner_node == "UNDECIDED":
                fail_reason = " (동점 규칙)"
            
            print(f"판정: {actual} | expected: {expected} | {status}{fail_reason}")
            
            results.append({'id': key, 'result': status, 'actual': actual, 'expected': expected, 'reason': fail_reason})
            performance_records.append({'size': int(size_val), 'time': measure_average_time(pattern_data, f_cross)})

        except Exception as e:
            print(f"- -- {key} --- 에러 발생: {e}")
            results.append({'id': key, 'result': 'FAIL', 'reason': str(e)})

    # --- [3] 성능 분석 섹션 ---
    print("\n#" + "-"*40)
    print("# [3] 성능 분석 (평균/10회)")
    print("#" + "-"*40)
    print(f"{'크기':<10} {'평균 시간(ms)':<15} {'연산 횟수':<10}")
    print("-" * 40)
    
    unique_sizes = sorted(list(set(r['size'] for r in performance_records)))
    # 3x3은 사용자 입력 모드에서 측정된 값을 쓰거나 별도 테스트 데이터를 통해 출력
    for size in unique_sizes:
        times = [r['time'] for r in performance_records if r['size'] == size]
        avg_time = sum(times) / len(times)
        print(f"{size}x{size:<7} {avg_time:<15.3f} {size*size:<10}")

    # --- [4] 결과 요약 섹션 ---
    print("\n#" + "-"*40)
    print("# [4] 결과 요약")
    print("#" + "-"*40)
    total = len(results)
    pass_cnt = sum(1 for r in results if r['result'] == 'PASS')
    fail_cnt = total - pass_cnt
    
    print(f"총 테스트: {total}개")
    print(f"통과: {pass_cnt}개")
    print(f"실패: {fail_cnt}개")
    
    if fail_cnt > 0:
        print("\n실패 케이스:")
        for r in results:
            if r['result'] == 'FAIL':
                reason_msg = "동점(UNDECIDED) 처리 규칙에 따라 FAIL" if "동점" in r['reason'] else r['reason']
                print(f"- {r['id']}: {reason_msg}")

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