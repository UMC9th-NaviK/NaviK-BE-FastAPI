"""
백엔드 KPI 폴백 계산 모듈.

설문 기반으로 KPI 점수를 계산하는 폴백 로직.
이력서에 근거가 부족한 KPI(basis="none")에 대해 사용.
"""
from typing import Dict, List

from app.domains.kpi.kpi_constants import BE_KPI_NAMES


# 선택값(1~5) → 점수(0~100) 변환
CHOICE_TO_SCORE = {
    1: 0,
    2: 25,
    3: 50,
    4: 75,
    5: 100
}

# 질문별 KPI 가중치 매핑
# Q_B1: 장애/문제 해결 상황
Q_B1_WEIGHTS = {
    10: 0.45,  # 운영·모니터링·장애 대응
    6: 0.25,   # 성능·트래픽 처리 최적화
    9: 0.20,   # 협업·문서화·의사결정 기록
    4: 0.10,   # 아키텍처 설계
}

# Q_B2: 기능 설계 & 협업
Q_B2_WEIGHTS = {
    2: 0.35,   # REST API 설계·구현
    3: 0.25,   # DB·데이터 모델링
    4: 0.20,   # 아키텍처 설계
    9: 0.20,   # 협업·문서화·의사결정 기록
}

# Q_B3: 배포·운영 환경 이해
Q_B3_WEIGHTS = {
    5: 0.45,   # 클라우드·DevOps 환경 이해
    10: 0.25,  # 운영·모니터링·장애 대응
    7: 0.15,   # 보안·인증·권한 처리
    8: 0.15,   # 테스트·코드 품질 관리
}

# Q_B4: 품질 & 개선 문화
Q_B4_WEIGHTS = {
    8: 0.45,   # 테스트·코드 품질 관리
    9: 0.25,   # 협업·문서화·의사결정 기록
    1: 0.15,   # 백엔드 기술 역량
    2: 0.15,   # REST API 설계·구현
}

# Q_B5: 문제 해결 방식
Q_B5_WEIGHTS = {
    6: 0.30,   # 성능·트래픽 처리 최적화
    8: 0.25,   # 테스트·코드 품질 관리
    4: 0.20,   # 아키텍처 설계
    9: 0.15,   # 협업·문서화·의사결정 기록
    3: 0.10,   # DB·데이터 모델링
}


def calculate_fallback_scores(
    q_b1: int,
    q_b2: int,
    q_b3: int,
    q_b4: int,
    q_b5: int
) -> Dict[int, Dict[str, any]]:
    """
    설문 응답 기반으로 KPI 점수 계산.
    
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
    # 선택값 → 점수 변환
    scores = {
        "q_b1": CHOICE_TO_SCORE.get(q_b1, 50),
        "q_b2": CHOICE_TO_SCORE.get(q_b2, 50),
        "q_b3": CHOICE_TO_SCORE.get(q_b3, 50),
        "q_b4": CHOICE_TO_SCORE.get(q_b4, 50),
        "q_b5": CHOICE_TO_SCORE.get(q_b5, 50),
    }
    
    # KPI별 가중치 합산
    # { kpi_id: [(점수, 가중치), ...] }
    kpi_contributions: Dict[int, List[tuple]] = {i: [] for i in range(1, 11)}
    
    # Q_B1 기여
    for kpi_id, weight in Q_B1_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b1"], weight))
    
    # Q_B2 기여
    for kpi_id, weight in Q_B2_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b2"], weight))
    
    # Q_B3 기여
    for kpi_id, weight in Q_B3_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b3"], weight))
    
    # Q_B4 기여
    for kpi_id, weight in Q_B4_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b4"], weight))
    
    # Q_B5 기여
    for kpi_id, weight in Q_B5_WEIGHTS.items():
        kpi_contributions[kpi_id].append((scores["q_b5"], weight))
    
    # KPI별 최종 점수 계산 (가중 평균)
    results = {}
    for kpi_id in range(1, 11):
        contributions = kpi_contributions[kpi_id]
        
        if contributions:
            # 가중 평균 계산
            total_weight = sum(w for _, w in contributions)
            weighted_sum = sum(s * w for s, w in contributions)
            final_score = round(weighted_sum / total_weight) if total_weight > 0 else 50
        else:
            # 해당 KPI에 기여하는 질문이 없는 경우 (현재 설계상 없음)
            final_score = 50
        
        # 0~100 범위 제한
        final_score = max(0, min(100, final_score))
        
        # 레벨 결정 (75~100: 상, 50~74: 중, 0~49: 하)
        if final_score >= 75:
            level = "high"
        elif final_score >= 50:
            level = "mid"
        else:
            level = "low"
        
        results[kpi_id] = {
            "score": final_score,
            "level": level,
            "kpi_name": BE_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}"),
            "source": "fallback"
        }
    
    return results
