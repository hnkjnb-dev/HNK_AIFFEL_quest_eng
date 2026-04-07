"""
한국어 감정분석 모델 로드 + 추론
"""

from transformers import pipeline


class SentimentAnalyzer:
    """
    Hugging Face pipeline 기반 한국어 감정분석기
    """

    def __init__(self, model_name: str = "daekeun-ml/koelectra-small-v3-nsmc"):
        self.model_name = model_name
        self.classifier = pipeline(
            task="text-classification",
            model=model_name,
            tokenizer=model_name,
        )

    def predict(self, review: str) -> dict:
        result = self.classifier(review, truncation=True, max_length=512)[0]

        raw_label = str(result["label"]).strip()
        score = float(result["score"])

        normalized = raw_label.upper()

        if normalized in {"1", "POS", "POSITIVE", "LABEL_1"}:
            label = "긍정"
        elif normalized in {"0", "NEG", "NEGATIVE", "LABEL_0"}:
            label = "부정"
        else:
            label = raw_label

        return {
            "label": label,
            "confidence": round(score, 4),
            "raw_label": raw_label,
            "model_name": self.model_name,
        }