"""
KPI 평가 서비스.

파이프라인:
1. 사용자가 경력/이력서 텍스트 입력
2. LLM이 직접 10개 KPI에 대해 점수 평가 (Few-shot Learning)
3. 상위 3개(강점), 하위 3개(약점) KPI 추출
4. analyze/abilities API: 모든 직군에서 각 KPI 근거 문장(reason)을 text-embedding-3-small로 임베딩하여 abilities로 반환
"""
from typing import List

from app.domains.kpi.scorer import calculate_kpi_scores, get_top_bottom_kpis
from app.schemas.kpi import (
    ResumeAnalysisResponse,
    AnalyzeAbilitiesResponse,
    KPIScoreItem,
    AbilityItem,
)
from app.ai.embedding import get_embeddings


def analyze_resume(resume_text: str, role: str = "backend") -> ResumeAnalysisResponse:
    """
    이력서 분석 및 KPI 점수 계산 (기존 API: reason/embedding 없음).
    """
    kpi_scores = calculate_kpi_scores(resume_text, role=role)
    strengths, weaknesses = get_top_bottom_kpis(kpi_scores)

    scores = [
        KPIScoreItem(
            kpi_id=kpi_id,
            kpi_name=kpi_scores[kpi_id]["kpi_name"],
            score=kpi_scores[kpi_id]["score"],
            level=kpi_scores[kpi_id]["level"],
            basis=kpi_scores[kpi_id].get("basis", "explicit"),
        )
        for kpi_id in sorted(kpi_scores.keys())
    ]

    return ResumeAnalysisResponse(
        scores=scores,
        strengths=strengths,
        weaknesses=weaknesses,
    )


def analyze_resume_abilities(resume_text: str, role: str) -> AnalyzeAbilitiesResponse:
    """
    이력서 분석 + KPI 순서별 abilities(근거 문장·임베딩) 반환.
    POST /api/kpi/analyze/abilities/{role} 전용.
    """
    kpi_scores = calculate_kpi_scores(resume_text, role=role)
    strengths, weaknesses = get_top_bottom_kpis(kpi_scores)

    ordered_ids = sorted(kpi_scores.keys())
    scores = [
        KPIScoreItem(
            kpi_id=kpi_id,
            kpi_name=kpi_scores[kpi_id]["kpi_name"],
            score=kpi_scores[kpi_id]["score"],
            level=kpi_scores[kpi_id]["level"],
            basis=kpi_scores[kpi_id].get("basis", "explicit"),
        )
        for kpi_id in ordered_ids
    ]

    # abilities: 모든 직군에서 근거 문장·임베딩 (scores와 1:1 동일 순서)
    embeddings_by_kpi: dict[int, list[float]] = {}
    reasons_to_embed = [
        (kid, (kpi_scores[kid].get("reason") or "").strip())
        for kid in ordered_ids
        if (kpi_scores[kid].get("basis") or "").lower() != "none"
    ]
    to_embed = [(kid, r) for kid, r in reasons_to_embed if r]
    if to_embed:
        try:
            vectors = get_embeddings([r for _, r in to_embed])
            for (kid, _), vec in zip(to_embed, vectors):
                embeddings_by_kpi[kid] = vec
        except Exception:
            pass

    abilities: List[AbilityItem] = []
    for kpi_id in ordered_ids:
        data = kpi_scores[kpi_id]
        basis = (data.get("basis") or "").lower()
        no_basis = basis == "none"
        if not no_basis:
            content = (data.get("reason") or "").strip() or None
            embedding = embeddings_by_kpi.get(kpi_id)
        else:
            content = None
            embedding = None
        abilities.append(AbilityItem(content=content, embedding=embedding))

    return AnalyzeAbilitiesResponse(
        scores=scores,
        abilities=abilities,
        strengths=strengths,
        weaknesses=weaknesses,
    )
