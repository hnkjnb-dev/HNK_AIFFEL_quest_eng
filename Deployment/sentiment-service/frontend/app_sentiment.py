"""
한국어 리뷰 감정분석 Streamlit 프론트엔드
"""

import requests
import streamlit as st

st.set_page_config(
    page_title="한국어 감정분석기",
    page_icon="📝",
    layout="centered",
)

API_BASE = "http://localhost:8000"


def call_predict_api(review: str, api_key: str) -> tuple[bool, dict]:
    try:
        response = requests.post(
            f"{API_BASE}/predict",
            json={"review": review},
            headers={"X-API-Key": api_key},
            timeout=60,
        )
    except requests.exceptions.ConnectionError:
        return False, {"detail": "FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요."}
    except requests.exceptions.Timeout:
        return False, {"detail": "요청 시간이 초과되었습니다."}
    except Exception as e:
        return False, {"detail": f"알 수 없는 오류: {str(e)}"}

    try:
        data = response.json()
    except Exception:
        return False, {"detail": f"JSON 응답 파싱 실패: {response.text}"}

    if response.status_code == 200:
        return True, data

    return False, data


st.title("한국어 영화/상품 후기 감정분석기")
st.caption("리뷰를 입력하면 긍정 / 부정과 신뢰도를 반환합니다.")

with st.sidebar:
    st.header("설정")
    api_key = st.text_input("API Key", value="test-key-001", type="password")
    st.markdown("테스트용 키 예시: `test-key-001`")

review = st.text_area(
    "리뷰 입력",
    height=180,
    placeholder="예: 배송이 빠르고 성능도 좋아서 매우 만족합니다.",
)

predict_button = st.button("감정 분석 실행", use_container_width=True)

if predict_button:
    if not review.strip():
        st.warning("리뷰를 입력해 주세요.")
    elif not api_key.strip():
        st.warning("API Key를 입력해 주세요.")
    else:
        with st.spinner("감정분석 중입니다..."):
            ok, result = call_predict_api(review, api_key)

        if ok:
            st.success("분석 완료")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("감정 결과", result["label"])
            with col2:
                st.metric("신뢰도", f'{result["confidence"]:.4f}')

            st.write("### 상세 정보")
            st.json(result)
        else:
            st.error("분석 실패")
            st.json(result)

st.markdown("---")
st.markdown("### 사용 방법")
st.markdown("1. 사이드바에 API Key 입력")
st.markdown("2. 리뷰 작성")
st.markdown("3. 감정 분석 실행 버튼 클릭")