import random
import re

def generate_sequence():
    a = random.randint(-20, 20)
    d = 0
    while d == 0:  # 공차가 0이면 등차수열이 아님
        d = random.randint(-10, 10)
    sequence = [a + d * i for i in range(5)]
    return sequence, a, d

def parse_user_input(expr, n):
    """
    사용자가 입력한 식을 안전하게 평가.
    예: -3n + 2 → -3*n + 2
    """
    expr = expr.lower().replace('^', '**')
    expr = re.sub(r'(?<!\*)\b(\d*)n\b', r'\1*n', expr)  # 3n → 3*n, n → 1*n
    expr = expr.replace(' ', '')
    try:
        return eval(expr, {"__builtins__": {}}, {"n": n})
    except Exception:
        return None

def check_answer(user_expr, a, d):
    for n in range(1, 6):
        expected = a + (n - 1) * d
        user_val = parse_user_input(user_expr, n)
        if user_val != expected:
            return False
    return True

def format_answer(a, d):
    c = a - d
    if d == 1:
        return f"aₙ = n + ({c})"
    elif d == -1:
        return f"aₙ = -n + ({c})"
    else:
        return f"aₙ = {d}n + ({c})"

def main():
    print("🎮 등차수열 일반항 맞히기 게임 🎮")
    print("일반항을 n에 대한 식으로 입력하세요. (예: 4n - 1, -2*n + 3)")
    print("게임 종료: 'quit' 입력\n")

    score = 0

    while True:
        sequence, a, d = generate_sequence()
        print(f"\n수열: {sequence}")
        user_input = input("aₙ = ")

        if user_input.strip().lower() == 'quit':
            print("게임을 종료합니다. 👋")
            break

        if check_answer(user_input, a, d):
            print("✅ 정답입니다!")
            score += 1
        else:
            print("❌ 오답입니다.")
            print(f"→ 정답 예시: {format_answer(a, d)}")

        print(f"현재 점수: {score}")
        print("------------------------------------------------")

if __name__ == "__main__":
    main()
