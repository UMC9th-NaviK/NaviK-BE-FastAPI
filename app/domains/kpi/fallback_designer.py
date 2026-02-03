"""
디자이너 KPI 폴백 계산 모듈.

설문 기반으로 KPI 점수를 계산하는 폴백 로직.
이력서에 근거가 부족한 KPI(basis="none")에 대해 사용.
"""
from typing import Dict, List

from app.domains.kpi.kpi_constants import DESIGNER_KPI_NAMES


CHOICE_TO_SCORE = {
    1: 0,
    2: 25,
    3: 50,
    4: 75,
    5: 100
}

# Q_DES_B1: 문제 재정의 & UX 전략 수립
Q_B1_WEIGHTS = {
    1: 0.45,   # UX 전략·문제 재정의
    2: 0.20,   # 정보 구조·사용자 플로우 설계
    9: 0.20,   # 협업·커뮤니케이션 역량
    10: 0.15,  # BX·BI 브랜드 경험 설계
}

# Q_DES_B2: 정보 구조 & 사용자 흐름 구체화
Q_B2_WEIGHTS = {
    2: 0.45,   # 정보 구조·사용자 플로우 설계
    1: 0.20,   # UX 전략·문제 재정의
    8: 0.20,   # 멀티 플랫폼(OS·Web·App) 이해
    9: 0.15,   # 협업·커뮤니케이션 역량
}

# Q_DES_B3: 프로토타이핑 & 인터랙션 검증
Q_B3_WEIGHTS = {
    4: 0.40,   # 프로토타이핑·인터랙션 구현
    3: 0.20,   # UI 시각 디자인·비주얼 완성도
    1: 0.20,   # UX 전략·문제 재정의
    9: 0.20,   # 협업·커뮤니케이션 역량
}

# Q_DES_B4: 디자인 시스템 & 협업 구조
Q_B4_WEIGHTS = {
    5: 0.45,   # 디자인 시스템 구축·운영
    3: 0.20,   # UI 시각 디자인·비주얼 완성도
    9: 0.20,   # 협업·커뮤니케이션 역량
    8: 0.15,   # 멀티 플랫폼(OS·Web·App) 이해
}

# Q_DES_B5: 근거 기반 UX 개선
Q_B5_WEIGHTS = {
    6: 0.40,   # 데이터 기반 UX 개선
    1: 0.20,   # UX 전략·문제 재정의
    9: 0.20,   # 협업·커뮤니케이션 역량
    4: 0.20,   # 프로토타이핑·인터랙션 구현
}


def calculate_fallback_scores(
    q_b1: int,
    q_b2: int,
    q_b3: int,
    q_b4: int,
    q_b5: int
) -> Dict[int, Dict[str, any]]:
    """
    설문 응답 기반으로 디자이너 KPI 점수 계산.

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
            "kpi_name": DESIGNER_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}"),
            "source": "fallback"
        }

    return results
