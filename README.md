# NaviK Backend Sub

## 기술 스택

- **Python**: 3.11+
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Package Manager**: pip

## 프로젝트 구조

```
app/
├── main.py              # FastAPI 앱 진입점
├── core/                # 핵심 설정 및 유틸리티
│   ├── config.py        # 환경변수 설정
│   ├── database.py      # 데이터베이스 연결
│   └── security.py      # 보안 유틸리티
├── models/              # SQLAlchemy 모델
│   ├── kpi.py          # KPI 정의 모델
│   ├── resume.py       # 이력서 분석 결과 모델
│   ├── question.py     # 질문 세트 모델
│   └── example.py      # KPI별 예시 모델 (상/중/하)
├── schemas/             # Pydantic 스키마
│   ├── kpi.py          # KPI 평가 스키마
│   └── resume.py       # 이력서 관련 스키마
├── domains/             # 도메인별 비즈니스 로직
│   └── kpi/            # KPI 평가 도메인
│       ├── router.py   # API 라우터
│       ├── service.py  # 비즈니스 로직 조율
│       ├── analyzer.py # 이력서 분석 (Resume Layer)
│       ├── scorer.py   # 예시 기반 유사도 점수 계산
│       ├── question_set.py  # 질문 세트 관리 (Q&A Layer)
│       └── fusion.py   # 신뢰도 가중 최종 점수 계산 (Fusion Layer)
├── ai/                  # AI/LLM 관련 유틸리티
│   ├── llm.py          # LLM 호출
│   ├── embeddings.py   # 임베딩 생성 및 유사도 계산
│   └── prompts.py      # 프롬프트 템플릿
└── utils/               # 공통 유틸리티
```

## 설치 및 실행

### 1. 가상환경 생성 및 활성화

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경변수 설정

`.env.example` 파일을 참고하여 `.env` 파일을 생성하고 필요한 환경변수를 설정.

```bash
cp .env.example .env
# .env 파일을 편집하여 실제 값 입력
```

### 4. 데이터베이스 설정

PostgreSQL 데이터베이스를 생성하고 `.env` 파일의 `DATABASE_URL`을 설정.

### 5. 서버 실행

```bash
uvicorn app.main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행.

## API 문서

서버 실행 후 다음 URL에서 API 문서를 확인할 수 있음:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 헬스체크

```bash
curl http://localhost:8000/health
```

## 핵심 기능

### KPI 평가 시스템

BE 직무별 KPI 10개를 평가하는 시스템.

1. **Resume Layer (이력서 분석)**

   - 이력서 PDF/텍스트를 분석하여 각 KPI별 점수(0~100) 산출
   - 이력서 신뢰도(0~1) 계산

2. **Q&A Layer (질문 세트)**

   - 고정 질문 세트를 통한 KPI 보완 평가
   - Set A: 1:1 질문 세트 (KPI 1개 ↔ 질문 1개)
   - Set B: 혼합 질문 세트 (질문 1개가 여러 KPI에 연결)

3. **Fusion Layer (신뢰도 가중)**

   - 신뢰도에 따라 이력서 점수 vs Q&A 점수 비율 결정
   - KPI별 최종 점수 계산 및 강점/약점 KPI 추출

4. **예시 기반 유사도 평가**
   - KPI별 상/중/하 예시와 지원자 경험을 비교
   - 임베딩/LLM 유사도를 기반으로 점수 산출
