"""
KPI 평가 서비스.

파이프라인:
1. 사용자가 경력/이력서 텍스트 입력
2. LLM이 직접 10개 KPI에 대해 점수 평가 (Few-shot Learning)
3. 상위 3개(강점), 하위 3개(약점) KPI 추출
"""
from typing import List

from app.domains.kpi.scorer import calculate_kpi_scores, get_top_bottom_kpis
from app.schemas.kpi import ResumeAnalysisResponse, KPIScoreResult


def analyze_resume(resume_text: str) -> ResumeAnalysisResponse:
    """
    이력서 분석 및 KPI 점수 계산.
    
    LLM 직접 평가 방식 사용:
    - Few-shot 예시를 통해 LLM이 기준을 학습
    - 동일한 기준으로 새 이력서를 평가
    - 점수는 40~90 범위 (상: 75~90, 중: 55~70, 하: 40~50)
    
    Args:
        resume_text: 이력서 텍스트
    
    Returns:
        분석 결과 (점수, 강점, 약점)
    """
    # LLM 직접 평가
    kpi_scores = calculate_kpi_scores(resume_text)
    
    # 상위/하위 KPI 추출
    strengths, weaknesses = get_top_bottom_kpis(kpi_scores)
    
    # 결과 변환
    scores = [
        KPIScoreResult(
            kpi_id=kpi_id,
            kpi_name=data["kpi_name"],
            score=data["score"],
            level=data["level"]
        )
        for kpi_id, data in kpi_scores.items()
    ]
    
    return ResumeAnalysisResponse(
        scores=scores,
        strengths=strengths,
        weaknesses=weaknesses
    )
