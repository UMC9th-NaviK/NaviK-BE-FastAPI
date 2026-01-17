# NaviK Backend Sub

## 기술 스택

- **Python**: 3.11+
- **Framework**: FastAPI
- **AI**: OpenAI GPT-4o-mini (Few-shot Learning 기반 KPI 평가)
- **Package Manager**: pip

## 프로젝트 구조

```
app/
├── main.py              # FastAPI 앱 진입점
├── core/                # 핵심 설정 및 유틸리티
│   ├── config.py        # 환경변수 설정
│   └── security.py      # 보안 유틸리티
├── schemas/             # Pydantic 스키마
│   └── kpi.py          # KPI 평가 스키마
├── domains/             # 도메인별 비즈니스 로직
│   └── kpi/            # KPI 평가 도메인
│       ├── router.py   # API 라우터
│       ├── service.py  # 비즈니스 로직 조율
│       ├── scorer.py   # 점수 계산 및 강점/약점 추출
│       └── kpi_constants.py  # KPI 상수 정의
├── ai/                  # AI/LLM 관련 유틸리티
│   ├── llm_backend.py  # 백엔드 KPI LLM 직접 평가
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

`.env` 파일을 생성하고 필요한 환경변수를 설정.

```bash
# .env 파일 예시
OPENAI_API_KEY=your_openai_api_key_here
DEBUG=True
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

### 4. 서버 실행

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

**LLM 직접 평가 방식 (Few-shot Learning)**

- 이력서 텍스트를 입력받아 GPT-4o-mini가 직접 10개 KPI에 대해 점수 산출
- Few-shot 예시를 통해 평가 기준 학습
- 점수 범위: 40~90 (상: 75~90, 중: 55~70, 하: 40~50)
- 강점 KPI 상위 3개, 약점 KPI 하위 3개 자동 추출

**API 엔드포인트**

```
POST /api/kpi/analyze/backend
Content-Type: application/json

{
  "resume_text": "이력서 텍스트..."
}
```

**응답 예시**

```json
{
  "scores": [
    {"kpi_id": 1, "kpi_name": "주력 언어·프레임워크 숙련도", "score": 85, "level": "high"},
    ...
  ],
  "strengths": [1, 3, 5],
  "weaknesses": [7, 8, 2]
}
```
