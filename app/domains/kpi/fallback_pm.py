"""
PM(Product Manager) KPI 폴백 계산 모듈.

설문 기반으로 KPI 점수를 계산하는 폴백 로직.
이력서에 근거가 부족한 KPI(basis="none")에 대해 사용.
"""
from typing import Dict, List

from app.domains.kpi.kpi_constants import PM_KPI_NAMES


CHOICE_TO_SCORE = {
    1: 0,
    2: 25,
    3: 50,
    4: 75,
    5: 100
}

# Q_PM_B1: 문제 정의 & 가설 수립
Q_B1_WEIGHTS = {
    1: 0.40,   # 문제 정의·가설 수립
    2: 0.25,   # 데이터 기반 의사결정
    10: 0.20,  # 사용자 리서치·공감
    7: 0.15,   # 실행력·오너십
}

# Q_PM_B2: 데이터 기반 판단 & 우선순위 도출
Q_B2_WEIGHTS = {
    2: 0.45,   # 데이터 기반 의사결정
    6: 0.25,   # 우선순위·스코프 관리
    1: 0.15,   # 문제 정의·가설 수립
    8: 0.15,   # 의사결정 정렬·협업 조율
}

# Q_PM_B3: 서비스 구조 & 핵심 플로우 결정
Q_B3_WEIGHTS = {
    3: 0.45,   # 서비스 구조·핵심 플로우 결정
    4: 0.20,   # 요구사항 정의·정책 설계
    8: 0.20,   # 의사결정 정렬·협업 조율
    7: 0.15,   # 실행력·오너십
}

# Q_PM_B4: 요구사항 정의 & 정책 문서화
Q_B4_WEIGHTS = {
    4: 0.45,   # 요구사항 정의·정책 설계
    3: 0.20,   # 서비스 구조·핵심 플로우 결정
    8: 0.20,   # 의사결정 정렬·협업 조율
    7: 0.15,   # 실행력·오너십
}

# Q_PM_B5: 실험·검증 기반 의사결정
Q_B5_WEIGHTS = {
    5: 0.40,   # 실험·검증 기반 의사결정
    2: 0.25,   # 데이터 기반 의사결정
    1: 0.20,   # 문제 정의·가설 수립
    7: 0.15,   # 실행력·오너십
}


def calculate_fallback_scores(
    q_b1: int,
    q_b2: int,
    q_b3: int,
    q_b4: int,
    q_b5: int
) -> Dict[int, Dict[str, any]]:
    """
    설문 응답 기반으로 PM KPI 점수 계산.

    Args:
        q_b1~q_b5: 각 질문에 대한 응답 (1~5)

    Returns:
        { kpi_id: { "score", "level", "kpi_name", "source" } }
    """
    scores = {
        "q_b1": CHOICE_TO_SCORE.get(q_b1, 50),
        "q_b2": CHOICE_TO_SCORE.get(q_b2, 50),
        "q_b3": CHOICE_TO_SCORE.get(q_b3, 50),
        "q_b4": CHOICE_TO_SCORE.get(q_b4, 50),
        "q_b5": CHOICE_TO_SCORE.get(q_b5, 50),
    }

    kpi_contributions: Dict[int, List[tuple]] = {i: [] for i in range(1, 11)}

    for kpi_id, weight in Q_B1_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b1"], weight))
    for kpi_id, weight in Q_B2_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b2"], weight))
    for kpi_id, weight in Q_B3_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b3"], weight))
    for kpi_id, weight in Q_B4_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b4"], weight))
    for kpi_id, weight in Q_B5_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b5"], weight))

    results = {}
    for kpi_id in range(1, 11):
        contributions = kpi_contributions[kpi_id]

        if contributions:
            total_weight = sum(w for _, w in contributions)
            weighted_sum = sum(s * w for s, w in contributions)
            final_score = round(weighted_sum / total_weight) if total_weight > 0 else 50
        else:
            final_score = 50

        final_score = max(0, min(100, final_score))

        if final_score >= 75:
            level = "high"
        elif final_score >= 50:
            level = "mid"
        else:
            level = "low"

        results[kpi_id] = {
            "score": final_score,
            "level": level,
            "kpi_name": PM_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}"),
            "source": "fallback"
        }

    return results
