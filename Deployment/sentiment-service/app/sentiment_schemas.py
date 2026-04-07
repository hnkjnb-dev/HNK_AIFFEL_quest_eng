"""
한국어 감정분석 API 스키마
"""

from pydantic import BaseModel, Field, field_validator


class SentimentRequest(BaseModel):
    review: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="감정분석할 한국어 리뷰 텍스트",
    )

    @field_validator("review")
    @classmethod
    def validate_review(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("리뷰는 공백만 입력할 수 없습니다.")
        return cleaned

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "review": "배송도 빠르고 제품 품질도 좋아서 정말 만족합니다."
                }
            ]
        }
    }


class SentimentResponse(BaseModel):
    success: bool = Field(description="요청 처리 성공 여부")
    label: str = Field(description="최종 감정 라벨 (긍정/부정)")
    confidence: float = Field(description="예측 신뢰도")
    raw_label: str = Field(description="모델 원본 라벨")
    model_name: str = Field(description="사용된 모델 이름")
    user: str = Field(description="인증된 사용자")
    input_text: str = Field(description="입력된 리뷰 텍스트")