import streamlit as st
import importlib.util
import os
import subprocess

# 파일 경로 설정
CHATBOT_SCRIPT = "./keyword_extraction_chatbot.ipynb"
BOOK_SEARCH_SCRIPT = "./book_search_using_naverAPI.py"

# .ipynb 파일을 .py로 변환
def convert_notebook_to_script(notebook_path):
    converted_path = notebook_path.replace(".ipynb", ".py")
    if not os.path.exists(converted_path):
        subprocess.run(["jupyter", "nbconvert", "--to", "script", notebook_path])
    return converted_path

# 파이썬 스크립트 동적 로드
def load_script(script_path):
    spec = importlib.util.spec_from_file_location("module_name", script_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    st.title("📚 키워드 기반 책 추천 챗봇")
    st.write("대화를 통해 키워드를 추출하고, 해당 키워드에 기반한 책을 추천해 드립니다!")

    # .ipynb 변환 후 스크립트 로드
    chatbot_script_path = convert_notebook_to_script(CHATBOT_SCRIPT)
    chatbot_module = load_script(chatbot_script_path)
    book_search_module = load_script(BOOK_SEARCH_SCRIPT)

    # API 키 로드
    NAVER_API_CLIENT_ID = os.getenv("NAVER_API_CLIENT_ID")
    NAVER_API_CLIENT_SECRET = os.getenv("NAVER_API_CLIENT_SECRET")

    # 사용자 입력 받기
    st.header("🗣 대화 시작")
    user_input = st.text_input("대화 메시지를 입력하세요:")
    if user_input:
        with st.spinner("키워드 추출 중..."):
            # 키워드 추출
            extracted_keywords = chatbot_module.wrapper_generate(
                chatbot_module.tokenizer, 
                chatbot_module.model, 
                chatbot_module.function_prepare_sample_text(chatbot_module.tokenizer, for_train=False)({'input': user_input})
            )
            st.text_area("📋 추출된 키워드:", extracted_keywords)

        # 책 추천
        st.header("📖 추천 도서")
        keywords = [kw.strip() for kw in extracted_keywords.split(",") if kw.strip()]
        if keywords:
            books = book_search_module.search_books_naver(NAVER_API_CLIENT_ID, NAVER_API_CLIENT_SECRET, keywords)
            if books:
                for idx, book in enumerate(books[:4]):
                    st.subheader(f"{idx + 1}. {book['title']}")
                    st.write(f"**저자**: {book['author']}")
                    st.write(f"**설명**: {book['description']}")
            else:
                st.warning("추천할 도서를 찾지 못했습니다. 😥")
        else:
            st.warning("키워드가 추출되지 않았습니다.")

if __name__ == "__main__":
    main()
