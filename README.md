# NaviK Backend API

> AI 기반 이력서 분석으로 직무별 KPI를 자동 평가하는 FastAPI 백엔드

<!-- 배지 추가 예정 -->
<!-- ![Build Status](https://img.shields.io/badge/build-passing-brightgreen) -->
<!-- ![Coverage](https://img.shields.io/badge/coverage-TBD-yellow) -->
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-009688)
![License](https://img.shields.io/badge/License-Unlicensed-lightgrey)

---

## Overview

### Why?

이력서를 직무별 역량 관점에서 정량적으로 평가하기란 쉽지 않습니다. 채용 담당자나 구직자 모두 "어떤 역량이 강하고 어디가 부족한지"를 객관적으로 파악하기 어렵습니다.

### What?

NaviK Backend는 **이력서 텍스트**를 입력받아 **GPT-4o-mini (Few-shot Learning)** 로 직무별 10개 KPI를 자동 평가하고, 강점/약점을 추출합니다. 이력서에 근거가 부족한 KPI에 대해서는 **설문 기반 폴백** 점수를 제공합니다.

---

## Features

- **4개 직무 지원** - 백엔드, 프론트엔드, PM, 디자이너 각각 10개 KPI 평가
- **LLM 직접 평가** - GPT-4o-mini Few-shot Learning으로 KPI별 점수(40~90) 산출
- **근거 수준 분류** - `explicit`(명시적) / `inferred`(간접 추론) / `none`(언급 없음)
- **강점/약점 자동 추출** - 상위 3개(강점), 하위 3개(약점) KPI 자동 분류
- **Abilities API** - KPI별 근거 문장 + text-embedding-3-small 임베딩(1536차원) 반환
- **설문 기반 폴백** - 이력서에 근거가 부족한 KPI를 5문항 설문으로 보완 평가
- **Docker 지원** - 컨테이너 기반 배포 가능

---

## Demo

> 스크린샷/데모 링크 추가 예정

서버 실행 후 Swagger UI에서 바로 테스트할 수 있습니다:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Getting Started

### Requirements

- **Python** 3.11+
- **OpenAI API Key** (GPT-4o-mini, text-embedding-3-small 사용)

### Installation

```bash
# 1. 저장소 클론
git clone https://github.com/UMC9th-NaviK/NaviK-BE-FastAPI.git
cd NaviK-BE-FastAPI

# 2. 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# 3. 의존성 설치
pip install -r requirements.txt
```

### Configuration

프로젝트 루트에 `.env` 파일을 생성합니다:

```bash
# .env
OPENAI_API_KEY=sk-your-openai-api-key
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000
```

| 변수 | 설명 | 기본값 |
|------|------|--------|
| `OPENAI_API_KEY` | OpenAI API 키 (필수) | - |
| `DEBUG` | 디버그 모드 | `False` |
| `SECRET_KEY` | 애플리케이션 시크릿 키 | - |
| `ALLOWED_ORIGINS` | CORS 허용 오리진 (쉼표 구분) | `http://localhost:3000,http://localhost:8000` |

> **주의**: `.env` 파일은 절대 Git에 커밋하지 마세요.

### Run

```bash
uvicorn app.main:app --reload
```

서버가 `http://localhost:8000`에서 실행됩니다.

**헬스체크:**
```bash
curl http://localhost:8000/health
# {"status": "healthy"}
```

---

## Usage

### 이력서 KPI 분석

```bash
curl -X POST http://localhost:8000/api/kpi/analyze/backend \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "3년차 백엔드 개발자입니다. Spring Boot와 JPA를 활용한 REST API 개발 경험이 있으며..."}'
```

**응답 예시:**
```json
{
  "scores": [
    {"kpi_id": 1, "kpi_name": "백엔드 기술 역량", "score": 85, "level": "high", "basis": "explicit"},
    {"kpi_id": 2, "kpi_name": "REST API 설계·구현", "score": 80, "level": "high", "basis": "explicit"},
    {"kpi_id": 3, "kpi_name": "DB·데이터 모델링", "score": 60, "level": "mid", "basis": "inferred"}
  ],
  "strengths": [1, 2, 5],
  "weaknesses": [7, 8, 10]
}
```

### Abilities API (근거 문장 + 임베딩)

```bash
curl -X POST http://localhost:8000/api/kpi/analyze/abilities/backend \
  -H "Content-Type: application/json" \
  -d '{"resume_text": "이력서 텍스트..."}'
```

### 폴백 평가 (설문 기반)

이력서에 근거가 부족한 KPI에 대해 1~5점 설문으로 보완:

```bash
curl -X POST http://localhost:8000/api/kpi/fallback/backend \
  -H "Content-Type: application/json" \
  -d '{"q_b1": 4, "q_b2": 3, "q_b3": 5, "q_b4": 2, "q_b5": 4}'
```

---

## API Reference

서버 실행 후 자동 생성되는 문서를 참조하세요:

| 문서 | URL |
|------|-----|
| Swagger UI | `http://localhost:8000/docs` |
| ReDoc | `http://localhost:8000/redoc` |

### 엔드포인트 요약

| Method | Path | 설명 |
|--------|------|------|
| `GET` | `/health` | 헬스체크 |
| `POST` | `/api/kpi/analyze/backend` | 백엔드 이력서 KPI 분석 |
| `POST` | `/api/kpi/analyze/frontend` | 프론트엔드 이력서 KPI 분석 |
| `POST` | `/api/kpi/analyze/pm` | PM 이력서 KPI 분석 |
| `POST` | `/api/kpi/analyze/designer` | 디자이너 이력서 KPI 분석 |
| `POST` | `/api/kpi/analyze/abilities/{role}` | KPI 분석 + 근거 문장·임베딩 반환 |
| `POST` | `/api/kpi/fallback/backend` | 백엔드 폴백 평가 (설문) |
| `POST` | `/api/kpi/fallback/frontend` | 프론트엔드 폴백 평가 (설문) |
| `POST` | `/api/kpi/fallback/designer` | 디자이너 폴백 평가 (설문) |
| `POST` | `/api/kpi/fallback/pm` | PM 폴백 평가 (설문) |

---

## Architecture

### 기술 스택

| 구분 | 기술 |
|------|------|
| Language | Python 3.11+ |
| Framework | FastAPI 0.104 |
| AI/LLM | OpenAI GPT-4o-mini (Few-shot), text-embedding-3-small |
| Validation | Pydantic v2 |
| Server | Uvicorn |
| Container | Docker |

### 디렉토리 구조

```
app/
├── main.py                    # FastAPI 앱 진입점
├── core/                      # 핵심 설정
│   ├── config.py              # 환경변수 설정 (pydantic-settings)
│   └── security.py            # 보안 유틸리티
├── schemas/                   # Pydantic 스키마 (요청/응답 모델)
│   ├── kpi.py                 # KPI 평가 스키마
│   ├── analysis.py
│   ├── experience.py
│   └── resume.py
├── domains/                   # 도메인별 비즈니스 로직
│   └── kpi/
│       ├── router.py          # API 라우터
│       ├── service.py         # 비즈니스 로직 조율
│       ├── scorer.py          # 점수 계산 및 강점/약점 추출
│       ├── kpi_constants.py   # KPI 상수 정의 (4개 직무)
│       ├── fusion.py          # 점수 융합 로직
│       ├── question_set.py    # 설문 질문셋
│       ├── fallback_backend.py   # 백엔드 폴백 로직
│       ├── fallback_frontend.py  # 프론트엔드 폴백 로직
│       ├── fallback_designer.py  # 디자이너 폴백 로직
│       └── fallback_pm.py        # PM 폴백 로직
├── ai/                        # AI/LLM 관련
│   ├── embedding.py           # text-embedding-3-small 임베딩
│   ├── prompts.py             # 프롬프트 템플릿
│   ├── llm_backend.py         # 백엔드 KPI LLM 평가
│   ├── llm_frontend.py        # 프론트엔드 KPI LLM 평가
│   ├── llm_pm.py              # PM KPI LLM 평가
│   └── llm_designer.py        # 디자이너 KPI LLM 평가
├── models/                    # 데이터 모델
└── utils/                     # 공통 유틸리티
    ├── text_processor.py
    └── validators.py
```

### 평가 파이프라인

```
이력서 텍스트 입력
       ↓
LLM Few-shot 평가 (GPT-4o-mini)
       ↓
KPI별 점수(40~90) + 근거 수준(explicit/inferred/none) + 근거 문장
       ↓
강점(상위 3개) / 약점(하위 3개) 추출
       ↓
[Abilities API] 근거 문장 → text-embedding-3-small 임베딩(1536차원)
       ↓
[근거 부족 시] 설문 폴백 → 가중 평균으로 KPI 보완 점수 산출
```

---

## Deployment

### Docker

```bash
# 빌드
docker build -t navik-backend .

# 실행
docker run -d -p 8000:8000 --env-file .env navik-backend
```

---

## Troubleshooting

| 증상 | 원인 | 해결 |
|------|------|------|
| `OPENAI_API_KEY` 관련 에러 | API 키 미설정 | `.env` 파일에 유효한 키 설정 |
| CORS 에러 | 프론트엔드 오리진 미등록 | `ALLOWED_ORIGINS`에 프론트엔드 URL 추가 |
| 점수가 모두 45점 | LLM 응답 파싱 실패 | OpenAI API 키 유효성 확인, 로그 확인 |
| 임베딩 `null` 반환 | `basis="none"`인 KPI | 정상 동작 (근거 없는 KPI는 임베딩 미생성) |

---

## Contributing

1. 이 저장소를 Fork 합니다.
2. Feature 브랜치를 생성합니다. (`git checkout -b feature/my-feature`)
3. 변경사항을 커밋합니다. (`git commit -m "feat: add my feature"`)
4. 브랜치에 Push 합니다. (`git push origin feature/my-feature`)
5. Pull Request를 생성합니다.

---

## License

라이선스 미지정 상태입니다. 프로젝트 오너에게 문의하세요.

---

## Support

- **Issues**: [GitHub Issues](https://github.com/UMC9th-NaviK/NaviK-BE-FastAPI/issues)
- **Organization**: UMC 9th - NaviK Team

---

## Credits

- [FastAPI](https://fastapi.tiangolo.com/)
- [OpenAI API](https://platform.openai.com/) (GPT-4o-mini, text-embedding-3-small)
- [Pydantic](https://docs.pydantic.dev/)
- UMC 9th NaviK Team
