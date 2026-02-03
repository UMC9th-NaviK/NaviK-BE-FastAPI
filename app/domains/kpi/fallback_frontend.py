"""
프론트엔드 KPI 폴백 계산 모듈.

설문 기반으로 KPI 점수를 계산하는 폴백 로직.
이력서에 근거가 부족한 KPI(basis="none")에 대해 사용.
"""
from typing import Dict, List

from app.domains.kpi.kpi_constants import FE_KPI_NAMES


# 선택값(1~5) → 점수(0~100) 변환
CHOICE_TO_SCORE = {
    1: 0,
    2: 25,
    3: 50,
    4: 75,
    5: 100
}

# Q_FE_B1: 컴포넌트 설계 & 상태 관리
Q_B1_WEIGHTS = {
    3: 0.40,   # 상태관리·컴포넌트 아키텍처
    2: 0.25,   # 프레임워크 숙련도
    1: 0.20,   # 웹 기본기
    8: 0.15,   # Git·PR·협업 프로세스 이해
}

# Q_FE_B2: API 연동 & 비동기 흐름
Q_B2_WEIGHTS = {
    5: 0.40,   # API 연동·비동기 처리
    3: 0.20,   # 상태관리·컴포넌트 아키텍처
    9: 0.20,   # 사용자 중심 UI 개발
    1: 0.20,   # 웹 기본기
}

# Q_FE_B3: 성능 최적화 경험
Q_B3_WEIGHTS = {
    4: 0.45,   # 웹 성능 최적화
    1: 0.20,   # 웹 기본기
    10: 0.20,  # 빌드·도구 환경 이해
    2: 0.15,   # 프레임워크 숙련도
}

# Q_FE_B4: 사용자 중심 UI 구현
Q_B4_WEIGHTS = {
    9: 0.45,   # 사용자 중심 UI 개발
    1: 0.20,   # 웹 기본기
    6: 0.20,   # 반응형·크로스 브라우징 대응
    8: 0.15,   # Git·PR·협업 프로세스 이해
}

# Q_FE_B5: 품질 관리 & 협업 문화
Q_B5_WEIGHTS = {
    7: 0.40,   # 테스트 코드·품질 관리
    8: 0.30,   # Git·PR·협업 프로세스 이해
    2: 0.15,   # 프레임워크 숙련도
    10: 0.15,  # 빌드·도구 환경 이해
}


def calculate_fallback_scores(
    q_b1: int,
    q_b2: int,
    q_b3: int,
    q_b4: int,
    q_b5: int
) -> Dict[int, Dict[str, any]]:
    """
    설문 응답 기반으로 프론트엔드 KPI 점수 계산.

    Args:
        q_b1~q_b5: 각 질문에 대한 응답 (1~5)

    Returns:
        {
            kpi_id: {
                "score": 점수 (0~100),
                "level": "high/mid/low",
                "kpi_name": KPI 이름,
                "source": "fallback"
            }
        }
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
            "kpi_name": FE_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}"),
            "source": "fallback"
        }

    return results
