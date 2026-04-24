import json
import time

def mac(pattern, filt):
    answer = 0
    n = len(pattern)
    for i in range(n):
        for j in range(n):
            answer += pattern[i][j] * filt[i][j]
    return answer

def decide(score_cross, score_x, epsilon=1e-9):
    answer = ""
    if abs(score_cross-score_x) < epsilon:
        answer = "UNDECIDED"
    elif score_cross > score_x:
        answer = "Cross"
    else:
        answer = "X"
    return answer

def is_valid_matrix(matrix, n):
    if not isinstance(matrix, list):
        return False
    if len(matrix) != n:
        return False
    for row in matrix:
        if not isinstance(row, list):
            return False
        if len(row) != n:
            return False
    return True

def input_matrix(n):
    matrix = []
    for i in range(n):
        while True:
            row = input(f"{i+1}번째 줄 입력: ").split()
            if len(row) != n:
                print(f"입력 형식 오류: 각 줄에 {n}개의 숫자를 공백으로 구분해 입력하세요.")
                continue
            try:
                row = [int(x) for x in row]
                matrix.append(row)
                break
            except ValueError:
                print("입력 형식 오류: 숫자만 입력하세요.")
    return matrix

def normalize(label):
    if label == "+":
        return "Cross"
    elif label.lower() == "x":
        return "X"
    else:
        return label

def measure_mac_time(pattern, filt, repeat=10000):
    start = time.perf_counter()
    for _ in range(repeat):
        mac(pattern, filt)
    end = time.perf_counter()
    answer = ((end-start)/repeat)*1000
    return answer

def run_performance_analysis(filters):
    print("\n===== 성능 분석 =====")
    print("크기\t 평균 시간(ms)\t연산 횟수")
    sizes = [3, 5, 13, 25]
    for size in sizes:
        filter_cross = filters[f"size_{size}"]["cross"]
        avg_time = measure_mac_time(filter_cross, filter_cross)
        operation_count = size*size
        print(f"{size}x{size}\t{avg_time: .6f}\t\t{operation_count}")

def run_user_mode():
    print("=== Cross 필터 입력 ===")
    filter_cross = input_matrix(3)
    print("=== X 필터 입력 ===")
    filter_x = input_matrix(3)
    print("=== 패턴 입력 ===")
    pattern = input_matrix(3)
    
    score_cross = mac(pattern, filter_cross)
    score_x = mac(pattern, filter_x)
    result = decide(score_cross, score_x)

    print("Cross 점수: ", score_cross)
    print("X 점수: ", score_x)
    if result == "UNDECIDED":
        print("판정: UNDECIDED (두 점수 차이가 매우 작음)")
    else: 
        print("판정: ", result)

def run_json_mode():
    with open("data.json", "r") as f:
        data = json.load(f)
    filters = data["filters"]
    patterns = data["patterns"]
    total_count = 0
    pass_count = 0
    fail_count = 0
    fail_cases = []
    for key, value in patterns.items():
        total_count += 1
        print("\n===== 현재 테스트:", key, "=====")
        size = int(key.split("_")[1])
        filter_cross = filters[f"size_{size}"]["cross"]
        filter_x = filters[f"size_{size}"]["x"]
        pattern = value["input"]
        expected = normalize(value["expected"])
        if not is_valid_matrix(pattern, size):
            print("FAIL - 패턴 크기 불일치")
            fail_count += 1
            fail_cases.append(f"{key}: 패턴 크기 불일치")
            continue
        if not is_valid_matrix(filter_cross, size):
            print("FAIL - Cross 필터 크기 불일치")
            fail_count += 1
            fail_cases.append(f"{key}: Cross 필터 크기 불일치")
            continue
        if not is_valid_matrix(filter_x, size):
            print("FAIL - X 필터 크기 불일치")
            fail_count += 1
            fail_cases.append(f"{key}: X 필터 크기 불일치")
            continue
        score_cross = mac(pattern, filter_cross)
        score_x = mac(pattern, filter_x)
        result = decide(score_cross, score_x)
        print("Cross 점수:", score_cross)
        print("X 점수:", score_x)
        print("결과:", result)
        print("정답:", expected)
        if result == expected:
            print("PASS")
            pass_count += 1
        else:
            print("FAIL")
            fail_count += 1
            fail_cases.append(key)
    print("\n===== 결과 요약 =====")
    print("총 테스트:", total_count)
    print("통과:", pass_count)
    print("실패:", fail_count)
    if fail_cases:
        print("실패 케이스:")
        for case in fail_cases:
            print("-", case)
    run_performance_analysis(filters)

if __name__ == "__main__":
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("선택: ")
    if choice == "1":
        run_user_mode()
    elif choice == "2":
        run_json_mode()
    else:
        print("잘못된 입력입니다.")