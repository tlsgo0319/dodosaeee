import streamlit as st
import random
import re

st.set_page_config(page_title="등차수열 일반항 게임", layout="centered")

# 수열 생성 함수
def generate_sequence():
    a = random.randint(-20, 20)
    d = 0
    while d == 0:
        d = random.randint(-10, 10)
    sequence = [a + d * i for i in range(5)]
    return sequence, a, d

# 사용자 입력 수식 평가
def parse_user_input(expr, n):
    expr = expr.lower().replace('^', '**')
    expr = re.sub(r'(?<!\*)\b(\d*)n\b', r'\1*n', expr)  # 3n → 3*n, n → 1*n
    expr = expr.replace(' ', '')
    try:
        return eval(expr, {"__builtins__": {}}, {"n": n})
    except Exception:
        return None

# 정답 체크 함수
def check_answer(user_expr, a, d):
    for n in range(1, 6):
        expected = a + (n - 1) * d
        user_val = parse_user_input(user_expr, n)
        if user_val != expected:
            return False
    return True

# 정답 포맷 표시
def format_answer(a, d):
    c = a - d
    if d == 1:
        return f"aₙ = n + ({c})"
    elif d == -1:
        return f"aₙ = -n + ({c})"
    else:
        return f"aₙ = {d}n + ({c})"

# Streamlit UI
st.title("🎮
