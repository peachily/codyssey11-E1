import json
from quiz import Quiz

def get_default_quizzes():
    quiz_list = [
        Quiz(
            "내 이름은?",
            ["지수", "현서", "수정", "예주"],
            3
        ),
        Quiz(
            "내가 가장 좋아하는 과일은?",
            ["딸기", "복숭아", "귤", "체리"],
            2
        ),
        Quiz(
            "내가 가장 좋아하는 영화는?",
            ["비포 선라이즈", "어벤져스", "인터스텔라", "라라랜드"],
            1
        ),
        Quiz(
            "내가 가장 많이 하는 게임은?",
            ["리그오브레전드", "메이플스토리", "TFT", "하스스톤"],
            4
        ),
        Quiz(
            "내 취미가 아닌 것은?",
            ["독서", "베이킹", "배드민턴", "음악 감상"],
            3
        )
    ]
    return quiz_list

class QuizGame:
    def __init__(self):
        self.quiz_list = get_default_quizzes()
        self.best_score = 0

    def show_menu(self):
        print("="*40)
        print("     🎯 나만의 퀴즈 게임 🎯")
        print(""*40)
        print("1. 퀴즈 풀기")
        print("2. 퀴즈 목록 보기")
        print("3. 퀴즈 추가하기")
        print("4. 최고 점수 확인")
        print("5. 종료")
        print("="*40)

    def get_menu_choice(self):
        while True:
            try:
                choice = input("선택: ").strip()
                if choice == "":
                    print("⚠️ 빈 입력입니다. 1~5 사이의 숫자를 입력하세요.")
                    continue
                choice = int(choice)
                if 1 <= choice <= 5:
                    return choice
                else:
                    print("⚠️ 1~5 사이의 숫자를 입력하세요.")
            except ValueError:
                print("⚠️ 1~5 사이의 숫자를 입력하세요.")

    def start_quiz(self):
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
            return

        score = 0
        print(f"\n📝 퀴즈를 시작합니다! (총 {len(self.quiz_list)}문제)")

        for i, quiz in enumerate(self.quiz_list, start=1):
            print("\n" + "-"*40)
            print(f"[문제 {i}]")
            quiz.display()

            while True:
                try:
                    answer = input("\n정답 입력: ").strip()

                    if answer == "":
                        print("⚠️ 빈 입력입니다. 1~4 사이의 숫자를 입력하세요.")
                        continue

                    answer = int(answer)
                    if 1 <= answer <= 4:
                        break
                    else:
                        print("⚠️ 1~4 사이의 숫자를 입력하세요.")

                except ValueError:
                    print("⚠️ 1~4 사이의 숫자를 입력하세요.")

            if quiz.is_correct(answer):
                print("✅ 정답입니다!")
                score += 1
            else:
                print(f"❌ 오답입니다! 정답은 {quiz.answer}번입니다.")

        final_score = int((score/len(self.quiz_list))*100)
        print("\n" + "="*40)
        print(f"🏆 결과: {len(self.quiz_list)}문제 중 {score}문제 정답! ({final_score}점)")

        if final_score > self.best_score:
            self.best_score = final_score
            print("🎉 새로운 최고 점수입니다!")

        print("="*40)

    def show_quiz_list(self):
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
            return
        print(f"\n📋 등록된 퀴즈 목록 (총 {len(self.quiz_list)}개)\n")
        print("-"*40)
        for i, quiz in enumerate(self.quiz_list, start=1):
            print(f"[{i}] {quiz.question}")
        print("-"*40)

    def add_quiz(self):
        print("\n📌 새로운 퀴즈를 추가합니다.")

        question = input("문제를 입력하세요: ").strip()
        if question == "":
            print("⚠️ 문제는 비워둘 수 없습니다.")
            return

        choices = []
        for i in range(1, 5):
            choice = input(f"선택지 {i}: ").strip()
            if choice == "":
                print("⚠️ 선택지는 비워둘 수 없습니다.")
                return
            choices.append(choice)

        while True:
            try:
                answer = input("정답 번호 (1~4): ").strip()

                if answer == "":
                    print("⚠️ 빈 입력입니다. 1~4 사이의 숫자를 입력하세요.")
                    continue

                answer = int(answer)
                if 1 <= answer <= 4:
                    break
                else:
                    print("⚠️ 1-4 사이의 숫자를 입력하세요.")

            except ValueError:
                print("⚠️ 1-4 사이의 숫자를 입력하세요.")

        new_quiz = Quiz(question, choices, answer)
        self.quiz_list.append(new_quiz)
        print("✅ 퀴즈가 추가되었습니다!")

    def show_best_score(self):
        if self.best_score == 0:
            print("아직 기록된 최고 점수가 없습니다.")
        else:
            print(f"🏆 최고 점수: {self.best_score}점")
    
    def save_state(self):
        data = {
            "quizzes": [quiz.to_dict() for quiz in self.quiz_list],
            "best_score": self.best_score
        }

        with open("state.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def run(self):
        while True:
            self.show_menu()
            choice = self.get_menu_choice()

            if choice == 1:
                self.start_quiz()
            elif choice == 2:
                self.show_quiz_list()
            elif choice == 3:
                self.add_quiz()
            elif choice == 4:
                self.show_best_score()
            elif choice == 5:
                self.save_state()
                print("게임을 종료합니다.")
                break