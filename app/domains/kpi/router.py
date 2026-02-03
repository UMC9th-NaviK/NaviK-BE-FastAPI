"""
KPI domain API routes.
"""
from fastapi import APIRouter, HTTPException

from app.domains.kpi.service import analyze_resume
from app.domains.kpi.fallback_backend import calculate_fallback_scores
from app.domains.kpi.fallback_frontend import calculate_fallback_scores as calculate_frontend_fallback_scores
from app.domains.kpi.fallback_designer import calculate_fallback_scores as calculate_designer_fallback_scores
from app.domains.kpi.fallback_pm import calculate_fallback_scores as calculate_pm_fallback_scores
from app.schemas.kpi import (
    ResumeAnalysisRequest, 
    ResumeAnalysisResponse,
    BackendFallbackRequest,
    BackendFallbackResponse,
    FrontendFallbackRequest,
    FrontendFallbackResponse,
    DesignerFallbackRequest,
    DesignerFallbackResponse,
    PMFallbackRequest,
    PMFallbackResponse,
    FallbackKPIScore
)

router = APIRouter()


@router.post("/analyze/backend", response_model=ResumeAnalysisResponse)
async def analyze_backend_resume_endpoint(
    request: ResumeAnalysisRequest
):
    """
    백엔드 개발자 이력서 분석 및 KPI 점수 계산.
    
    이력서 텍스트를 입력받아 각 KPI별 점수를 계산하고,
    강점/약점 KPI를 추출합니다.
    """
    try:
        result = analyze_resume(request.resume_text, role="backend")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")


@router.post("/analyze/frontend", response_model=ResumeAnalysisResponse)
async def analyze_frontend_resume_endpoint(
    request: ResumeAnalysisRequest
):
    """
    프론트엔드 개발자 이력서 분석 및 KPI 점수 계산.
    
    이력서 텍스트를 입력받아 각 KPI별 점수를 계산하고,
    강점/약점 KPI를 추출합니다.
    """
    try:
        result = analyze_resume(request.resume_text, role="frontend")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")


@router.post("/analyze/pm", response_model=ResumeAnalysisResponse)
async def analyze_pm_resume_endpoint(
    request: ResumeAnalysisRequest
):
    """
    PM(Product Manager) 이력서 분석 및 KPI 점수 계산.
    
    이력서 텍스트를 입력받아 각 KPI별 점수를 계산하고,
    강점/약점 KPI를 추출합니다.
    """
    try:
        result = analyze_resume(request.resume_text, role="pm")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")


@router.post("/analyze/designer", response_model=ResumeAnalysisResponse)
async def analyze_designer_resume_endpoint(
    request: ResumeAnalysisRequest
):
    """
    디자이너(Designer) 이력서 분석 및 KPI 점수 계산.
    
    이력서 텍스트를 입력받아 각 KPI별 점수를 계산하고,
    강점/약점 KPI를 추출합니다.
    """
    try:
        result = analyze_resume(request.resume_text, role="designer")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")


# ===== 폴백 API =====

@router.post("/fallback/backend", response_model=BackendFallbackResponse)
async def backend_fallback_endpoint(
    request: BackendFallbackRequest
):
    """
    백엔드 KPI 폴백 평가 (설문 기반).
    
    이력서에 근거가 부족한 KPI(basis="none")에 대해
    설문 응답을 기반으로 점수를 계산합니다.
    
    ## 질문 설명
    - Q_B1: 장애/문제 해결 경험 (1~5)
    - Q_B2: 기능 설계 & 협업 경험 (1~5)
    - Q_B3: 배포·운영 환경 이해 (1~5)
    - Q_B4: 품질 & 개선 문화 경험 (1~5)
    - Q_B5: 문제 해결 방식 (1~5)
    
    ## 점수 변환
    - 1점 → 0, 2점 → 25, 3점 → 50, 4점 → 75, 5점 → 100
    """
    try:
        kpi_scores = calculate_fallback_scores(
            q_b1=request.q_b1,
            q_b2=request.q_b2,
            q_b3=request.q_b3,
            q_b4=request.q_b4,
            q_b5=request.q_b5
        )
        
        scores = [
            FallbackKPIScore(
                kpi_id=kpi_id,
                kpi_name=data["kpi_name"],
                score=data["score"],
                level=data["level"],
                source=data["source"]
            )
            for kpi_id, data in sorted(kpi_scores.items())
        ]
        
        return BackendFallbackResponse(
            scores=scores,
            raw_inputs={
                "q_b1": request.q_b1,
                "q_b2": request.q_b2,
                "q_b3": request.q_b3,
                "q_b4": request.q_b4,
                "q_b5": request.q_b5
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"폴백 계산 중 오류 발생: {str(e)}")


@router.post("/fallback/frontend", response_model=FrontendFallbackResponse)
async def frontend_fallback_endpoint(
    request: FrontendFallbackRequest
):
    """
    프론트엔드 KPI 폴백 평가 (설문 기반).

    이력서에 근거가 부족한 KPI(basis="none")에 대해
    설문 응답을 기반으로 점수를 계산합니다.

    ## 질문 설명
    - Q_B1: 컴포넌트 설계 & 상태 관리 (1~5)
    - Q_B2: API 연동 & 비동기 흐름 (1~5)
    - Q_B3: 성능 최적화 경험 (1~5)
    - Q_B4: 사용자 중심 UI 구현 (1~5)
    - Q_B5: 품질 관리 & 협업 문화 (1~5)

    ## 점수 변환
    - 1점 → 0, 2점 → 25, 3점 → 50, 4점 → 75, 5점 → 100
    """
    try:
        kpi_scores = calculate_frontend_fallback_scores(
            q_b1=request.q_b1,
            q_b2=request.q_b2,
            q_b3=request.q_b3,
            q_b4=request.q_b4,
            q_b5=request.q_b5
        )

        scores = [
            FallbackKPIScore(
                kpi_id=kpi_id,
                kpi_name=data["kpi_name"],
                score=data["score"],
                level=data["level"],
                source=data["source"]
            )
            for kpi_id, data in sorted(kpi_scores.items())
        ]

        return FrontendFallbackResponse(
            scores=scores,
            raw_inputs={
                "q_b1": request.q_b1,
                "q_b2": request.q_b2,
                "q_b3": request.q_b3,
                "q_b4": request.q_b4,
                "q_b5": request.q_b5
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"폴백 계산 중 오류 발생: {str(e)}")


@router.post("/fallback/designer", response_model=DesignerFallbackResponse)
async def designer_fallback_endpoint(
    request: DesignerFallbackRequest
):
    """
    디자이너 KPI 폴백 평가 (설문 기반).

    이력서에 근거가 부족한 KPI(basis="none")에 대해
    설문 응답을 기반으로 점수를 계산합니다.

    ## 질문 설명
    - Q_DES_B1: 문제 재정의 & UX 전략 수립 (1~5)
    - Q_DES_B2: 정보 구조 & 사용자 흐름 구체화 (1~5)
    - Q_DES_B3: 프로토타이핑 & 인터랙션 검증 (1~5)
    - Q_DES_B4: 디자인 시스템 & 협업 구조 (1~5)
    - Q_DES_B5: 근거 기반 UX 개선 (1~5)

    ## 점수 변환
    - 1점 → 0, 2점 → 25, 3점 → 50, 4점 → 75, 5점 → 100
    """
    try:
        kpi_scores = calculate_designer_fallback_scores(
            q_b1=request.q_b1,
            q_b2=request.q_b2,
            q_b3=request.q_b3,
            q_b4=request.q_b4,
            q_b5=request.q_b5
        )

        scores = [
            FallbackKPIScore(
                kpi_id=kpi_id,
                kpi_name=data["kpi_name"],
                score=data["score"],
                level=data["level"],
                source=data["source"]
            )
            for kpi_id, data in sorted(kpi_scores.items())
        ]

        return DesignerFallbackResponse(
            scores=scores,
            raw_inputs={
                "q_b1": request.q_b1,
                "q_b2": request.q_b2,
                "q_b3": request.q_b3,
                "q_b4": request.q_b4,
                "q_b5": request.q_b5
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"폴백 계산 중 오류 발생: {str(e)}")


@router.post("/fallback/pm", response_model=PMFallbackResponse)
async def pm_fallback_endpoint(
    request: PMFallbackRequest
):
    """
    PM KPI 폴백 평가 (설문 기반).

    이력서에 근거가 부족한 KPI(basis="none")에 대해
    설문 응답을 기반으로 점수를 계산합니다.

    ## 질문 설명
    - Q_PM_B1: 문제 정의 & 가설 수립 (1~5)
    - Q_PM_B2: 데이터 기반 판단 & 우선순위 도출 (1~5)
    - Q_PM_B3: 서비스 구조 & 핵심 플로우 결정 (1~5)
    - Q_PM_B4: 요구사항 정의 & 정책 문서화 (1~5)
    - Q_PM_B5: 실험·검증 기반 의사결정 (1~5)

    ## 점수 변환
    - 1점 → 0, 2점 → 25, 3점 → 50, 4점 → 75, 5점 → 100
    """
    try:
        kpi_scores = calculate_pm_fallback_scores(
            q_b1=request.q_b1,
            q_b2=request.q_b2,
            q_b3=request.q_b3,
            q_b4=request.q_b4,
            q_b5=request.q_b5
        )

        scores = [
            FallbackKPIScore(
                kpi_id=kpi_id,
                kpi_name=data["kpi_name"],
                score=data["score"],
                level=data["level"],
                source=data["source"]
            )
            for kpi_id, data in sorted(kpi_scores.items())
        ]

        return PMFallbackResponse(
            scores=scores,
            raw_inputs={
                "q_b1": request.q_b1,
                "q_b2": request.q_b2,
                "q_b3": request.q_b3,
                "q_b4": request.q_b4,
                "q_b5": request.q_b5
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"폴백 계산 중 오류 발생: {str(e)}")
