"""
한국어 리뷰 감정분석 FastAPI 서버
"""

import asyncio
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Depends, HTTPException

from app.auth import verify_api_key
from app.logger_config import setup_logger
from app.error_handlers import register_error_handlers
from app.middleware import RequestLoggingMiddleware
from app.sentiment_schemas import SentimentRequest, SentimentResponse
from app.sentiment_model import SentimentAnalyzer

logger = setup_logger("sentiment_api")

app = FastAPI(
    title="Korean Review Sentiment Analysis API",
    description="한국어 영화/상품 후기 감정분석 API (인증 필요)",
    version="1.0.0",
)

app.add_middleware(RequestLoggingMiddleware)
register_error_handlers(app)

inference_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="sentiment")

analyzer = None


@app.on_event("startup")
async def startup():
    global analyzer
    logger.info("감정분석 모델 로드 중...")
    analyzer = SentimentAnalyzer("daekeun-ml/koelectra-small-v3-nsmc")
    logger.info("감정분석 모델 로드 완료")


def run_predict(review: str) -> dict:
    if analyzer is None:
        raise RuntimeError("모델이 로드되지 않았습니다.")
    return analyzer.predict(review)


@app.get("/health", tags=["System"])
async def health_check():
    return {
        "status": "healthy" if analyzer is not None else "loading",
        "model": analyzer.model_name if analyzer is not None else None,
    }


@app.post("/predict", response_model=SentimentResponse, tags=["Prediction"])
async def predict_sentiment(
    request: SentimentRequest,
    user: str = Depends(verify_api_key),
):
    if analyzer is None:
        raise HTTPException(status_code=503, detail="모델이 아직 로드되지 않았습니다.")

    logger.info(f"감정분석 요청 - 사용자: {user}")

    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            inference_executor,
            run_predict,
            request.review,
        )
    except Exception as e:
        logger.exception("추론 실패")
        raise HTTPException(status_code=500, detail=f"모델 추론 실패: {str(e)}")

    return SentimentResponse(
        success=True,
        label=result["label"],
        confidence=result["confidence"],
        raw_label=result["raw_label"],
        model_name=result["model_name"],
        user=user,
        input_text=request.review,
    )