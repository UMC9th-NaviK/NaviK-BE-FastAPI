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
