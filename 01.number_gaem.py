import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(
    page_title="1-100 숫자 맞추기 게임",
    page_icon="🎮",
    layout="centered"
)

# 커스텀 CSS (디자인 강화)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #4F46E5;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    .sub-title {
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
    }
    .hint-box-up {
        background-color: #FEF3C7;
        color: #D97706;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #F59E0B;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .hint-box-down {
        background-color: #DBEAFE;
        color: #1D4ED8;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #3B82F6;
        font-weight: bold;
        font-size: 1.2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #D1FAE5;
        color: #047857;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #10B981;
        font-weight: bold;
        font-size: 1.3rem;
        text-align: center;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = random.randint(1, 100)
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'best_score' not in st.session_state:
    st.session_state.best_score = None
if 'history' not in st.session_state:
    st.session_state.history = []
if 'message' not in st.session_state:
    st.session_state.message = None
if 'msg_type' not in st.session_state:
    st.session_state.msg_type = None

def reset_game():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.attempts = 0
    st.session_state.game_over = False
    st.session_state.history = []
    st.session_state.message = None
    st.session_state.msg_type = None

# 상단 헤더 & 웰컴 메시지
st.markdown("<h1 class='main-title'>🎮 숫자 맞추기 게임 (Up & Down)</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>컴퓨터가 생각한 <b>1부터 100 사이의 숫자</b>를 맞춰보세요! 최소한의 시도 횟수로 성공하는 것이 목표입니다.</p>", unsafe_allow_html=True)

# 점수판 / 현황판
col1, col2 = st.columns(2)
with col1:
    st.metric(label="현재 시도 횟수", value=f"{st.session_state.attempts}회")
with col2:
    best_disp = f"{st.session_state.best_score}회" if st.session_state.best_score is not None else "없음"
    st.metric(label="🏆 최고 기록", value=best_disp)

st.divider()

# 게임 진행 구역
if not st.session_state.game_over:
    with st.form(key='guess_form', clear_on_submit=True):
        guess = st.number_input(
            "1부터 100 사이의 숫자를 입력하세요:",
            min_value=1,
            max_value=100,
            step=1,
            value=50
        )
        submit_button = st.form_submit_button(label="제출하기 🎯")

    if submit_button:
        st.session_state.attempts += 1
        secret = st.session_state.secret_number

        if guess < secret:
            st.session_state.message = f"📈 **Up!** {guess}보다 더 큰 숫자입니다."
            st.session_state.msg_type = "up"
            st.session_state.history.append((st.session_state.attempts, guess, "Up 📈"))
        elif guess > secret:
            st.session_state.message = f"📉 **Down!** {guess}보다 더 작은 숫자입니다."
            st.session_state.msg_type = "down"
            st.session_state.history.append((st.session_state.attempts, guess, "Down 📉"))
        else:
            st.session_state.game_over = True
            st.session_state.message = f"🎉 정답입니다! 정답은 **{secret}** 이었습니다! ({st.session_state.attempts}회 만에 성공)"
            st.session_state.msg_type = "success"
            st.session_state.history.append((st.session_state.attempts, guess, "정답! 🎉"))
            
            # 최고 기록 갱신 체크
            if st.session_state.best_score is None or st.session_state.attempts < st.session_state.best_score:
                st.session_state.best_score = st.session_state.attempts

        st.rerun()

# 힌트 및 메시지 출력
if st.session_state.message:
    if st.session_state.msg_type == "up":
        st.markdown(f"<div class='hint-box-up'>{st.session_state.message}</div>", unsafe_allow_html=True)
    elif st.session_state.msg_type == "down":
        st.markdown(f"<div class='hint-box-down'>{st.session_state.message}</div>", unsafe_allow_html=True)
    elif st.session_state.msg_type == "success":
        st.markdown(f"<div class='success-box'>{st.session_state.message}</div>", unsafe_allow_html=True)

# 게임 완료 시 다시 하기 버튼
if st.session_state.game_over:
    st.balloons()
    st.success("축하합니다! 게임을 완료하셨습니다.")
    if st.button("🔄 다시 도전하기", type="primary"):
        reset_game()
        st.rerun()

# 게임 리셋 버튼 & 히스토리
st.divider()
c_btn, c_space = st.columns([1, 2])
with c_btn:
    if st.button("️ 처음부터 다시 시작"):
        reset_game()
        st.rerun()

# 시도 기록 테이블 표시
if st.session_state.history:
    with st.expander("📋 나의 시도 기록 보기", expanded=True):
        st.table([
            {"시도": item[0], "입력한 숫자": item[1], "결과": item[2]}
            for item in reversed(st.session_state.history)
        ])
