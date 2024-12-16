import streamlit as st

# 페이지 설정
st.set_page_config(page_title="북메이트 📚", page_icon="📚", layout="centered")

# 앱 제목과 설명
st.title("📚 북메이트 - 책 추천 챗봇")
st.write("**당신의 취향에 맞는 책을 추천해드려요!** 원하는 책 장르나 주제를 알려주세요. 제가 맞춤형 책을 추천해 드릴게요!")

# 대화 기록 저장
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "안녕하세요! 어떤 책을 찾고 계신가요? 예: '재미있는 소설', '자기계발서' 등"}]

# 이전 대화 화면에 표시
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력 받기
if prompt := st.chat_input("책에 대해 무엇이든 물어보세요!"):
    # 사용자 메시지 저장 및 화면에 표시
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- 책 추천 모델 호출 부분 (여기만 교체하면 돼) ---
    # 현재는 예시 결과를 반환하도록 구성
    example_recommendations = [
        "책1: 예시 도서 1",
        "책2: 예시 도서 2",
        "책3: 예시 도서 3"
    ]
    response = f"이런 책들은 어떠세요?\n\n" + "\n".join([f"- {book}" for book in example_recommendations])

    # 챗봇 응답 저장 및 화면에 표시
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
