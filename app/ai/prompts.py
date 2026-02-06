"""
Prompt templates and management.
"""

# 모든 직군 KPI 평가에서 reason(근거 문장) 출력 형식을 통일하기 위한 공통 규칙
REASON_FORMAT_RULES = """
## reason(근거 문장) 작성 규칙 (필수)
- **한 문장만** 출력하고, 끝에 마침표(.) 하나로 끝낸다.
- **문체 통일**: 서술형으로 쓴다. 예: "~한 경험이 있다.", "~를 수행했다.", "~역할을 했다."
- **길이**: 20자 이상 80자 이하 (너무 짧거나 길지 않게).
- **내용**: 이력서에 나온 구체적 경험·기술·성과를 한 줄로 요약한다. 추상적 설명이나 점수 설명은 넣지 않는다.
- **인칭**: 지원자 관점으로 쓴다. ("~했다" / "~한 경험이 있다" 등)
- basis가 "none"인 KPI는 reason을 빈 문자열로 두거나, 이 규칙에 맞는 한 줄 요약만 쓴다.
"""


def normalize_reason(reason: str | None, max_length: int = 80) -> str | None:
    """
    LLM이 출력한 근거 문장을 일관된 형태로 정규화.
    - 앞뒤 공백 제거, 한 문장만 유지, 끝에 마침표 보장, 길이 제한.
    """
    if reason is None:
        return None
    s = reason.strip()
    if not s:
        return None
    # 첫 번째 마침표까지만 취해 한 문장으로
    first_period = s.find(".")
    if first_period != -1:
        s = s[: first_period + 1]
    if not s.endswith("."):
        s = s.rstrip() + "."
    s = s.strip()
    if len(s) > max_length:
        s = s[: max_length - 1].rsplit(" ", 1)[0] + "."
    return s if s != "." else None
