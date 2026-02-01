"""
KPI 상수 정의.

백엔드/프론트엔드/PM/디자이너 KPI ID와 이름 매핑을 하드코딩으로 관리.
"""

# 백엔드 KPI ID → 이름 매핑
BE_KPI_NAMES = {
    1: "백엔드 기술 역량",
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

# PM KPI ID → 이름 매핑
PM_KPI_NAMES = {
    1: "문제 정의·가설 수립",
    2: "데이터 기반 의사결정",
    3: "서비스 구조·핵심 플로우 결정",
    4: "요구사항 정의·정책 설계",
    5: "실험·검증 기반 의사결정",
    6: "우선순위·스코프 관리",
    7: "실행력·오너십",
    8: "의사결정 정렬·협업 조율",
    9: "AI/LLM 활용 기획",
    10: "사용자 리서치·공감",
}

# 디자이너 KPI ID → 이름 매핑
DESIGNER_KPI_NAMES = {
    1: "UX 전략·문제 재정의",
    2: "정보 구조·사용자 플로우 설계",
    3: "UI 시각 디자인·비주얼 완성도",
    4: "프로토타이핑·인터랙션 구현",
    5: "디자인 시스템 구축·운영",
    6: "데이터 기반 UX 개선",
    7: "AI 디자인 활용 능력",
    8: "멀티 플랫폼(OS·Web·App) 이해",
    9: "협업·커뮤니케이션 역량",
    10: "BX·BI 브랜드 경험 설계",
}




def get_kpi_name(kpi_id: int, role: str = "backend") -> str:
    """
    KPI ID로 이름 조회.
    
    Args:
        kpi_id: KPI ID (1~10)
        role: "backend", "frontend", "pm", 또는 "designer"
    
    Returns:
        KPI 이름
    """
    if role == "frontend":
        return FE_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}")
    elif role == "pm":
        return PM_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}")
    elif role == "designer":
        return DESIGNER_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}")
    else:
        return BE_KPI_NAMES.get(kpi_id, f"KPI {kpi_id}")
