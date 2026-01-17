"""
KPI 상수 정의.

백엔드/프론트엔드 KPI ID와 이름 매핑을 하드코딩으로 관리.
"""

# 백엔드 KPI ID → 이름 매핑
BE_KPI_NAMES = {
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

# 프론트엔드 KPI ID → 이름 매핑
FE_KPI_NAMES = {
    1: "웹 기본기",
    2: "프레임워크 숙련도",
    3: "상태관리·컴포넌트 아키텍처",
    4: "웹 성능 최적화",
    5: "API 연동·비동기 처리",
    6: "반응형·크로스 브라우징 대응",
    7: "테스트 코드·품질 관리",
    8: "Git·PR·협업 프로세스 이해",
    9: "사용자 중심 UI 개발",
    10: "빌드·도구 환경 이해",
}


def get_kpi_name(kpi_id: int, role: str = "backend") -> str:
    """
    KPI ID로 이름 조회.
    
    Args:
        kpi_id: KPI ID (1~10)
        role: "backend" 또는 "frontend"
    
    Returns:
        KPI 이름
    """
    if role == "frontend":
        return FE_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}")
    else:
        return BE_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}")
