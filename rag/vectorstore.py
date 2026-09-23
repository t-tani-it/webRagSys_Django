# -*- coding: utf-8 -*-
"""rag/vectorstore.py - チャンク保存と類似検索.

Why: RAGの保存・検索層を分離するため。
What: save_chunks、delete_chunks、searchを提供する。
Assumption / Dependencies: Django ORM。
I/O: 入力=文書ID＋チャンク＋ベクトル、出力=類似チャンク。
Caution: Python側でコサイン計算する（件数が少ない前提）。
Future Work: ベクトルDB連携。
Change Log: 初版作成。
"""

import math

from config import get_settings
from documents.models import DocumentChunk
from rag.embeddings import embed_query, embed_texts

settings = get_settings()

# 設定値ブロック（冒頭集約）
TOP_K = settings.top_k


def _cosine(a: list[float], b: list[float]) -> float:
    """コサイン類似度を計算する。

    Args:
        a: ベクトルA。
        b: ベクトルB。

    Returns:
        float: 類似度（1に近いほど類似）。
    """
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


def save_chunks(document_id: int, chunks: list[str]) -> None:
    """既存チャンクを置換して保存する。

    Args:
        document_id: 文書ID。
        chunks: チャンク一覧。

    Side Effects:
        DocumentChunk行を削除・挿入する。
    """
    # 解説：更新・削除時に古いベクトルが残らないよう、置換方式にする。
    DocumentChunk.objects.filter(document_id=document_id).delete()
    vectors = embed_texts(chunks)
    rows = [
        DocumentChunk(document_id=document_id, chunk_index=idx, content=chunk, embedding=vec)
        for idx, (chunk, vec) in enumerate(zip(chunks, vectors))
    ]
    DocumentChunk.objects.bulk_create(rows)


def delete_chunks(document_id: int) -> None:
    """文書のチャンクを削除する。

    Args:
        document_id: 文書ID。

    Side Effects:
        対象行を削除する。
    """
    DocumentChunk.objects.filter(document_id=document_id).delete()


def search(query: str, top_k: int = TOP_K) -> list[DocumentChunk]:
    """質問に類似したチャンクを返す。

    Args:
        query: 質問文。
        top_k: 取得件数。

    Returns:
        list[DocumentChunk]: 類似度順チャンク。

    Side Effects:
        なし（読取のみ）。
    """
    qvec = embed_query(query)
    rows = list(DocumentChunk.objects.all())
    scored = [(_cosine(qvec, list(r.embedding or [])), r) for r in rows]
    scored.sort(key=lambda x: x[0], reverse=True)
    return [r for _, r in scored[:top_k]]
