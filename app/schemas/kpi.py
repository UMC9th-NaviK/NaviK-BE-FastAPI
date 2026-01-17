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
    score: int = Field(..., description="점수 (45/65/85)")
    level: str = Field(..., description="high/mid/low")


class ResumeAnalysisRequest(BaseModel):
    """이력서 분석 요청."""
    resume_text: str = Field(..., description="이력서 텍스트")


class ResumeAnalysisResponse(BaseModel):
    """이력서 분석 응답."""
    scores: List[KPIScoreResult] = Field(..., description="KPI별 점수 결과")
    strengths: List[int] = Field(default_factory=list, description="강점 KPI ID 리스트 (상위 3개)")
    weaknesses: List[int] = Field(default_factory=list, description="약점 KPI ID 리스트 (하위 3개)")
