# 한국어 리뷰 감정분석 서비스
## 1. 프로젝트 소개
본 프로젝트는 한국어 영화 및 상품 후기를 입력하면 감정을 분석하여 **긍정 / 부정
결과와 신뢰도(confidence)**를 반환하는 서비스입니다.
FastAPI 기반의 백엔드와 Streamlit 기반의 프론트엔드를 결합하여 사용자 친화적인 AI
서비스를 구현하였습니다.
---
## 2. 선택한 태스크 및 도메인
* 도메인: 텍스트 처리 (NLP)
* 태스크: 감정 분석 (Text Classification)
사용자가 입력한 리뷰를 기반으로 감정을 분류하는 서비스를 구현하였습니다.
---
## 3. 사용 모델
* 모델: `daekeun-ml/koelectra-small-v3-nsmc`
* 특징:
* 한국어 감정 분석 특화 모델
* 가벼운 모델 크기로 CPU 환경에서도 빠른 추론 가능
* Hugging Face `pipeline()`으로 간단하게 사용 가능
---
## 4. 시스템 구조
### 백엔드 (FastAPI)
* `/predict` 엔드포인트 구현
* Pydantic 기반 입력 검증
* `run_in_executor`를 통한 비동기 추론
* API Key 인증 (`Depends(verify_api_key)`)
### 프론트엔드 (Streamlit)
* 사용자 입력 UI 제공
* API 호출 후 결과 시각화
---
## 5. 주요 기능
* 리뷰 입력 → 감정 분석 수행
* 결과: 긍정/부정 + 신뢰도 출력
* API Key 인증 적용 (401 처리)
* 잘못된 입력에 대한 에러 처리 (422 반환)
---
## 6. 실행 방법
### 1. 서버 실행
```bash
```
uvicorn app.sentiment_api:app --host 0.0.0.0 --port 8000 --reload
### 2. 프론트 실행
```bash
streamlit run frontend/app_sentiment.py --server.port 8501
```
---
## 7. 실행 결과
### Swagger 테스트
* 정상 요청: 200 OK 반환
* 인증 실패: 401 반환
### Streamlit
* 사용자 입력 → 결과 출력 정상 동작
---
## 8. 결론
본 프로젝트를 통해 FastAPI 기반 모델 서빙과 API 인증, 프론트엔드 연동까지 하나의
완성된 AI 서비스를 구현할 수 있었다.
