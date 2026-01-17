"""
백엔드 KPI 상수 정의.

KPI ID와 이름 매핑을 하드코딩으로 관리.
"""

# KPI ID → 이름 매핑
KPI_NAMES = {
    1: "주력 언어·프레임워크 숙련도",
    2: "REST API 설계·구현",
    3: "DB·데이터 모델링",
    4: "아키텍처 설계",
    5: "클라우드·DevOps 환경 이해",
    6: "성능·트래픽 처리 최적화",
    7: "보안·인증·권한 처리",
    8: "테스트·코드 품질 관리",
    9: "협업·문서화·의사결정 기록",
    10: "운영·모니터링·장애 대응",
}


def get_kpi_name(kpi_id: int) -> str:
    """KPI ID로 이름 조회."""
    return KPI_NAMES.get(kpi_id, f"KPI {kpi_id}")
