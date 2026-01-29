"""
KPI domain API routes.
"""
from fastapi import APIRouter, HTTPException

from app.domains.kpi.service import analyze_resume
from app.schemas.kpi import ResumeAnalysisRequest, ResumeAnalysisResponse

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
