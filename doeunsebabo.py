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
st.title("🎮 등차수열 일반항 맞히기 게임")
st.write("아래 수열의 일반항 aₙ을 n에 대한 식으로 맞혀보세요!")
st.markdown("*입력 예시*: `3n + 2`, `-2*n + 5`, `4*(n-1) - 3`")
st.markdown("종료하려면 **페이지를 닫거나 새로고침**하세요.")

# 세션 상태 초기화
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'sequence' not in st.session_state:
    st.session_state.sequence, st.session_state.a, st.session_state.d = generate_sequence()

# 문제 제시
st.subheader(f"수열: {st.session_state.sequence}")

# 사용자 입력
user_input = st.text_input("aₙ = ", key="user_input")

# 정답 판정
if st.button("제출"):
    if user_input.strip() == "":
        st.warning("수식을 입력해주세요.")
    elif check_answer(user_input, st.session_state.a, st.session_state.d):
        st.success("✅ 정답입니다!")
        st.session_state.score += 1
        st.session_state.sequence, st.session_state.a, st.session_state.d = generate_sequence()
        st.experimental_rerun()
    else:
        st.error("❌ 오답입니다.")
        st.info(f"정답 예시: {format_answer(st.session_state.a, st.session_state.d)}")
        st.session_state.sequence, st.session_state.a, st.session_state.d = generate_sequence()
        st.experimental_rerun()

# 점수 표시
st.metric("현재 점수", st.session_state.score)
