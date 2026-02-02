"""
KPI domain API routes.
"""
from fastapi import APIRouter, HTTPException

from app.domains.kpi.service import analyze_resume
from app.domains.kpi.fallback_backend import calculate_fallback_scores
from app.schemas.kpi import (
    ResumeAnalysisRequest, 
    ResumeAnalysisResponse,
    BackendFallbackRequest,
    BackendFallbackResponse,
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
