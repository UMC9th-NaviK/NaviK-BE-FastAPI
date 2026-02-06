"""
KPI 평가 관련 Pydantic 스키마.

KPI 평가 요청/응답, 점수 결과 등의 스키마를 정의.
"""
from typing import Optional, List
from pydantic import BaseModel, Field


class KPIScoreResult(BaseModel):
    """KPI 점수 결과."""
    kpi_id: int
    kpi_name: str
    score: int = Field(..., description="점수 (40~90)")
    level: str = Field(..., description="high/mid/low")
    basis: str = Field(
        default="explicit",
        description="근거 수준: explicit(명시적 언급), inferred(간접 추론), none(언급 없음)"
    )
    reason: Optional[str] = Field(
        default=None,
        description="해당 점수를 준 한 줄 근거 문장 (백엔드 분석 시에만 포함)"
    )
    embedding: Optional[List[float]] = Field(
        default=None,
        description="reason 문장의 text-embedding-3-small 임베딩 벡터(1536차원, 백엔드 분석 시에만 포함)"
    )


class ResumeAnalysisRequest(BaseModel):
    """이력서 분석 요청."""
    resume_text: str = Field(..., description="이력서 텍스트")


class ResumeAnalysisResponse(BaseModel):
    """이력서 분석 응답."""
    scores: List[KPIScoreResult] = Field(..., description="KPI별 점수 결과")
    strengths: List[int] = Field(default_factory=list, description="강점 KPI ID 리스트 (상위 3개)")
    weaknesses: List[int] = Field(default_factory=list, description="약점 KPI ID 리스트 (하위 3개)")


# ===== 폴백 로직용 스키마 =====

class BackendFallbackRequest(BaseModel):
    """백엔드 폴백 평가 요청 (설문 기반)."""
    q_b1: int = Field(..., ge=1, le=5, description="Q_B1: 장애/문제 해결 (1~5)")
    q_b2: int = Field(..., ge=1, le=5, description="Q_B2: 기능 설계 & 협업 (1~5)")
    q_b3: int = Field(..., ge=1, le=5, description="Q_B3: 배포·운영 환경 (1~5)")
    q_b4: int = Field(..., ge=1, le=5, description="Q_B4: 품질 & 개선 문화 (1~5)")
    q_b5: int = Field(..., ge=1, le=5, description="Q_B5: 문제 해결 방식 (1~5)")


class FallbackKPIScore(BaseModel):
    """폴백으로 계산된 KPI 점수."""
    kpi_id: int
    kpi_name: str
    score: int = Field(..., description="점수 (0~100, 가중 평균)")
    level: str = Field(..., description="high/mid/low")
    source: str = Field(default="fallback", description="점수 출처 (fallback)")


class BackendFallbackResponse(BaseModel):
    """백엔드 폴백 평가 응답."""
    scores: List[FallbackKPIScore] = Field(..., description="폴백으로 계산된 KPI 점수")
    raw_inputs: dict = Field(..., description="원본 입력값 (Q_B1~Q_B5)")


class FrontendFallbackRequest(BaseModel):
    """프론트엔드 폴백 평가 요청 (설문 기반)."""
    q_b1: int = Field(..., ge=1, le=5, description="Q_B1: 컴포넌트 설계 & 상태 관리 (1~5)")
    q_b2: int = Field(..., ge=1, le=5, description="Q_B2: API 연동 & 비동기 흐름 (1~5)")
    q_b3: int = Field(..., ge=1, le=5, description="Q_B3: 성능 최적화 경험 (1~5)")
    q_b4: int = Field(..., ge=1, le=5, description="Q_B4: 사용자 중심 UI 구현 (1~5)")
    q_b5: int = Field(..., ge=1, le=5, description="Q_B5: 품질 관리 & 협업 문화 (1~5)")


class FrontendFallbackResponse(BaseModel):
    """프론트엔드 폴백 평가 응답."""
    scores: List[FallbackKPIScore] = Field(..., description="폴백으로 계산된 KPI 점수")
    raw_inputs: dict = Field(..., description="원본 입력값 (q_b1~q_b5)")


class DesignerFallbackRequest(BaseModel):
    """디자이너 폴백 평가 요청 (설문 기반)."""
    q_b1: int = Field(..., ge=1, le=5, description="Q_DES_B1: 문제 재정의 & UX 전략 (1~5)")
    q_b2: int = Field(..., ge=1, le=5, description="Q_DES_B2: 정보 구조 & 사용자 흐름 (1~5)")
    q_b3: int = Field(..., ge=1, le=5, description="Q_DES_B3: 프로토타이핑 & 인터랙션 (1~5)")
    q_b4: int = Field(..., ge=1, le=5, description="Q_DES_B4: 디자인 시스템 & 협업 (1~5)")
    q_b5: int = Field(..., ge=1, le=5, description="Q_DES_B5: 근거 기반 UX 개선 (1~5)")


class DesignerFallbackResponse(BaseModel):
    """디자이너 폴백 평가 응답."""
    scores: List[FallbackKPIScore] = Field(..., description="폴백으로 계산된 KPI 점수")
    raw_inputs: dict = Field(..., description="원본 입력값 (q_b1~q_b5)")


class PMFallbackRequest(BaseModel):
    """PM 폴백 평가 요청 (설문 기반)."""
    q_b1: int = Field(..., ge=1, le=5, description="Q_PM_B1: 문제 정의 & 가설 수립 (1~5)")
    q_b2: int = Field(..., ge=1, le=5, description="Q_PM_B2: 데이터 기반 판단 & 우선순위 (1~5)")
    q_b3: int = Field(..., ge=1, le=5, description="Q_PM_B3: 서비스 구조 & 핵심 플로우 (1~5)")
    q_b4: int = Field(..., ge=1, le=5, description="Q_PM_B4: 요구사항 정의 & 정책 문서화 (1~5)")
    q_b5: int = Field(..., ge=1, le=5, description="Q_PM_B5: 실험·검증 기반 의사결정 (1~5)")


class PMFallbackResponse(BaseModel):
    """PM 폴백 평가 응답."""
    scores: List[FallbackKPIScore] = Field(..., description="폴백으로 계산된 KPI 점수")
    raw_inputs: dict = Field(..., description="원본 입력값 (q_b1~q_b5)")
