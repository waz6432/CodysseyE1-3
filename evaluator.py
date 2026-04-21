import time
from mac_logic import calculate_mac

def measure_average_time(pattern, filter_arr, iterations=10):
    # MAC 연산의 평균 실행 시간 측정 (ms 단위)
    start_time = time.perf_counter()
    for _ in range(iterations):
        calculate_mac(pattern, filter_arr)
    end_time = time.perf_counter()
    
    avg_time_ms = ((end_time - start_time) / iterations) * 1000
    return avg_time_ms