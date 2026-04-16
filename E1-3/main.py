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

if __name__ == "__main__":
    print("=== Mini NPU Simulator ===")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")
    choice = input("선택: ")
    if choice == "1":
        run_user_mode()
    elif choice == "2":
        print("...")
    else:
        print("잘못된 입력입니다.")