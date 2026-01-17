"""
KPI 점수 산출 모듈.

LLM 직접 평가 방식으로 이력서 텍스트에서 
백엔드 개발자 KPI 10개에 대한 점수를 산출.
"""

from typing import Dict, List, Tuple

from app.ai.llm_backend import evaluate_resume_kpis
from app.domains.kpi.kpi_constants import get_kpi_name


def calculate_kpi_scores(
    resume_text: str
) -> Dict[int, Dict[str, any]]:
    """
    이력서 텍스트에서 KPI별 점수 계산.
    
    Args:
        resume_text: 이력서 텍스트
    
    Returns:
        {
            kpi_id: {
                "score": 점수 (40~90),
                "level": "high/mid/low",
                "kpi_name": KPI 이름
            }
        }
    """
    # LLM으로 직접 평가
    scores = evaluate_resume_kpis(resume_text)
    
    results = {}
    for kpi_id, score in scores.items():
        kpi_name = get_kpi_name(kpi_id)
        
        # 레벨 결정 (75~90: 상, 55~70: 중, 40~50: 하)
        if score >= 75:
            level = "high"
        elif score >= 55:
            level = "mid"
        else:
            level = "low"  # 54점 이하
        
        results[kpi_id] = {
            "score": score,
            "level": level,
            "kpi_name": kpi_name
        }
    
    return results


def get_top_bottom_kpis(
    scores: Dict[int, Dict[str, any]],
    top_n: int = 3
) -> Tuple[List[int], List[int]]:
    """
    상위/하위 KPI ID 추출.
    
    Args:
        scores: calculate_kpi_scores의 결과
        top_n: 상위/하위 몇 개를 추출할지
    
    Returns:
        (강점 KPI ID 리스트, 약점 KPI ID 리스트)
    """
    # 점수순 정렬
    sorted_kpis = sorted(
        scores.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )
    
    # 상위 N개 (강점)
    strengths = [kpi_id for kpi_id, _ in sorted_kpis[:top_n]]
    
    # 하위 N개 (약점)
    weaknesses = [kpi_id for kpi_id, _ in sorted_kpis[-top_n:]]
    
    return strengths, weaknesses
