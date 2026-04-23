# 🎬 Netflix Recommendation System with Vertex AI Pipeline

## 프로젝트 개요

본 프로젝트는 Netflix Prize Dataset을 활용하여
사용자의 시청 이력을 기반으로 영화 평점을 예측하는 추천 시스템을 구축하고,
Google Cloud Vertex AI를 통해 **모델 학습부터 배포까지의 MLOps 파이프라인을 구현**하는 것을 목표로 합니다.

---

## 주요 기능

* 대규모 시계열 데이터 전처리 (Netflix Prize Dataset)
* Transformer 기반 추천 모델 구현
* 사용자 시퀀스 기반 평점 예측
* GCP (BigQuery, GCS, Vertex AI) 활용
* Kubeflow Pipeline 기반 자동화 파이프라인 구축
* Vertex AI Endpoint를 통한 모델 서빙 및 배포

---

## 전체 아키텍처

```
Kaggle Dataset
    ↓
Data Preprocessing (Colab)
    ↓
Google Cloud Storage (GCS)
    ↓
BigQuery 적재
    ↓
Vertex AI Pipeline
    ├── 데이터 추출
    ├── 모델 학습
    └── 모델 배포
    ↓
Vertex AI Endpoint (Serving)
```

---

## 모델 설명

* **모델 구조**: Transformer 기반 Recommendation Network
* **입력**: 사용자별 영화 시청 시퀀스
* **출력**: 마지막 영화에 대한 예상 평점

### 핵심 아이디어

* 사용자의 과거 시청 패턴을 시퀀스로 구성
* Transformer의 Self-Attention을 활용하여
  **사용자 선호 패턴 학습**

---

## 프로젝트 구조

```
.
├── pipeline_job.yaml        # Vertex AI Pipeline 정의
├── model.py                 # 모델 정의
├── handler.py               # 서빙 핸들러
├── model.pth                # 학습된 모델 가중치
├── *.pdf                    # 실험 및 구현 과정 (Colab 결과)
└── README.md
```

---

## 실행 방법

### 1. 환경 설정

```bash
pip install google-cloud-aiplatform kfp google-cloud-storage
```

### 2. GCP 설정

* Service Account 생성
* `credentials.json` 다운로드 후 설정

```bash
gcloud auth login --cred-file=credentials.json
```

---

### 3. Pipeline 실행

```python
from google.cloud import aiplatform

job = aiplatform.PipelineJob(
    display_name="netflix_recommender_pipeline",
    template_path="pipeline_job.yaml",
    pipeline_root="gs://YOUR_BUCKET/pipeline_root",
)

job.submit()
```

---

## 결과

* 학습 Loss 감소 확인 (Epoch별 안정적 수렴)
* 평균 정확도 약 **0.38 수준**
* Vertex AI Endpoint를 통한 실시간 예측 가능

---

## 배운 점

* 대규모 데이터 처리 시 샘플링 전략의 중요성
* Transformer가 추천 시스템에도 효과적으로 활용 가능함을 확인
* Vertex AI + Kubeflow Pipeline을 통한
  **End-to-End MLOps 흐름 경험**

---

## 보안 관련

* API Key, Service Account Key 등 민감 정보는 포함하지 않음
* 환경 변수 및 외부 파일(`credentials.json`)로 분리 관리

---

## 데이터 출처

* Netflix Prize Dataset
  https://www.kaggle.com/datasets/netflix-inc/netflix-prize-data

---

## 한 줄 정리

> 단순 모델 구현이 아닌,
> **데이터 → 학습 → 배포까지 이어지는 실제 MLOps 파이프라인을 구축한 프로젝트**


# AIFFEL Campus Online Code Peer Review Templete
- 코더 : 고길동
- 리뷰어 : 강백호


# PRT(Peer Review Template)
- [x]  **1. 주어진 문제를 해결하는 완성된 코드가 제출되었나요?**
    - 문제에서 요구하는 최종 결과물이 첨부되었는지 확인
        - 중요! 해당 조건을 만족하는 부분을 캡쳐해 근거로 첨부
    
- [ ]  **2. 전체 코드에서 가장 핵심적이거나 가장 복잡하고 이해하기 어려운 부분에 작성된 
주석 또는 doc string을 보고 해당 코드가 잘 이해되었나요?**
    - 해당 코드 블럭을 왜 핵심적이라고 생각하는지 확인
    - 해당 코드 블럭에 doc string/annotation이 달려 있는지 확인
    - 해당 코드의 기능, 존재 이유, 작동 원리 등을 기술했는지 확인
    - 주석을 보고 코드 이해가 잘 되었는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
- [x]  **3. 에러가 난 부분을 디버깅하여 문제를 해결한 기록을 남겼거나
새로운 시도 또는 추가 실험을 수행해봤나요?**
    - 문제 원인 및 해결 과정을 잘 기록하였는지 확인
    - 프로젝트 평가 기준에 더해 추가적으로 수행한 나만의 시도, 
    실험이 기록되어 있는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
- [ ]  **4. 회고를 잘 작성했나요?**
    - 주어진 문제를 해결하는 완성된 코드 내지 프로젝트 결과물에 대해
    배운점과 아쉬운점, 느낀점 등이 기록되어 있는지 확인
    - 전체 코드 실행 플로우를 그래프로 그려서 이해를 돕고 있는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부
        
- [ ]  **5. 코드가 간결하고 효율적인가요?**
    - 파이썬 스타일 가이드 (PEP8) 를 준수하였는지 확인
    - 코드 중복을 최소화하고 범용적으로 사용할 수 있도록 함수화/모듈화했는지 확인
        - 중요! 잘 작성되었다고 생각되는 부분을 캡쳐해 근거로 첨부

---

# 회고(참고 링크 및 코드 개선)
```
# 리뷰어의 회고를 작성합니다.
# 코드 리뷰 시 참고한 링크가 있다면 링크와 간략한 설명을 첨부합니다.
# 코드 리뷰를 통해 개선한 코드가 있다면 코드와 간략한 설명을 첨부합니다.
```
