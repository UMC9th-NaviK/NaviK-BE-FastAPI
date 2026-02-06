"""
KPI 평가 서비스.

파이프라인:
1. 사용자가 경력/이력서 텍스트 입력
2. LLM이 직접 10개 KPI에 대해 점수 평가 (Few-shot Learning)
3. 상위 3개(강점), 하위 3개(약점) KPI 추출
4. 백엔드 역할일 때: 각 KPI 근거 문장(reason)을 text-embedding-3-small로 임베딩하여 포함
"""
from typing import List

from app.domains.kpi.scorer import calculate_kpi_scores, get_top_bottom_kpis
from app.schemas.kpi import ResumeAnalysisResponse, KPIScoreResult
from app.ai.embedding import get_embeddings


def analyze_resume(resume_text: str, role: str = "backend") -> ResumeAnalysisResponse:
    """
    이력서 분석 및 KPI 점수 계산.
    
    LLM 직접 평가 방식 사용:
    - Few-shot 예시를 통해 LLM이 기준을 학습
    - 동일한 기준으로 새 이력서를 평가
    - 점수는 40~90 범위 (상: 75~90, 중: 55~70, 하: 40~50)
    
    Args:
        resume_text: 이력서 텍스트
        role: "backend", "frontend", "pm", 또는 "designer"
    
    Returns:
        분석 결과 (점수, 강점, 약점)
    """
    # LLM 직접 평가
    kpi_scores = calculate_kpi_scores(resume_text, role=role)

    # 상위/하위 KPI 추출
    strengths, weaknesses = get_top_bottom_kpis(kpi_scores)

    # reason 임베딩 수행 (basis가 none이면 근거 없음 → reason·embedding null)
    embeddings_by_kpi: dict[int, list[float]] = {}
    if role == "backend":
        ordered_ids = sorted(kpi_scores.keys())
        reasons = [
            (kid, (kpi_scores[kid].get("reason") or "").strip())
            for kid in ordered_ids
            if (kpi_scores[kid].get("basis") or "").lower() != "none"
        ]
        to_embed = [(kid, r) for kid, r in reasons if r]
        if to_embed:
            try:
                vectors = get_embeddings([r for _, r in to_embed])
                for (kid, _), vec in zip(to_embed, vectors):
                    embeddings_by_kpi[kid] = vec
            except Exception:
                pass  # 임베딩 실패 시 embedding 필드 없이 반환

    # 결과 변환 (basis가 none이거나 reason이 비어 있으면 reason·embedding은 null)
    scores = []
    for kpi_id, data in kpi_scores.items():
        basis = data.get("basis", "explicit")
        no_basis = (basis or "").lower() == "none"
        if role == "backend" and not no_basis:
            raw_reason = (data.get("reason") or "").strip()
            reason = raw_reason or None
        else:
            reason = None
        has_reason = bool(reason)
        embedding = embeddings_by_kpi.get(kpi_id) if (role == "backend" and has_reason) else None
        scores.append(
            KPIScoreResult(
                kpi_id=kpi_id,
                kpi_name=data["kpi_name"],
                score=data["score"],
                level=data["level"],
                basis=data.get("basis", "explicit"),
                reason=reason,
                embedding=embedding,
            )
        )

    return ResumeAnalysisResponse(
        scores=scores,
        strengths=strengths,
        weaknesses=weaknesses
    )
