"""
텍스트 임베딩 유틸.

OpenAI text-embedding-3-small(1536차원)로 문장 리스트를 임베딩.
"""
from typing import List

from openai import OpenAI

from app.core.config import settings

EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_DIMENSIONS = 1536


def get_embeddings(texts: List[str]) -> List[List[float]]:
    """
    문장 리스트를 text-embedding-3-small로 임베딩.

    Args:
        texts: 임베딩할 문자열 리스트 (빈 문자열은 제로 벡터로 처리)

    Returns:
        각 문장에 대한 1536차원 벡터 리스트 (입력 순서 유지)
    """
    if not texts:
        return []

    to_embed = [t.strip() if (t or "").strip() else " " for t in texts]
    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    resp = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=to_embed,
        dimensions=EMBEDDING_DIMENSIONS,
    )
    return [d.embedding for d in resp.data]
