# -*- coding: utf-8 -*-
"""tests/test_chat.py - AIチャットテスト.

Why: RAG回答の配線を保証するため。
What: 正常系2件＋異常系1件を提供する。
Assumption / Dependencies: pytest-django、DRFテストクライアント。
I/O: 入力=質問JSON、出力=回答JSON。
Caution: 偽実装のため外部通信しない。
Future Work: 出典スコア追加時の追従。
Change Log: 初版作成。
"""

import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def test_chat_answers_with_registered_document() -> None:
    """登録文書を根拠に偽LLMが回答する。"""
    client = APIClient()
    client.post(
        "/documents",
        {"title": "休暇規定", "content": "年次休暇は10日付与する。"},
        format="json",
    )
    res = client.post("/chat", {"question": "休暇は何日ですか。"}, format="json")
    assert res.status_code == 200
    data = res.json()
    # 解説：偽回答は定型文のため、前方一致でRAG配線を確認する。
    assert data["answer"].startswith("[FAKE回答]")
    assert data["source_ids"] == [1]


def test_chat_without_documents_returns_empty_sources() -> None:
    """未登録で質問すると根拠が空になる。"""
    client = APIClient()
    res = client.post("/chat", {"question": "休暇は何日ですか。"}, format="json")
    assert res.status_code == 200
    assert res.json()["source_ids"] == []


def test_chat_blank_question_returns_422() -> None:
    """空質問は422になる。"""
    client = APIClient()
    res = client.post("/chat", {"question": " "}, format="json")
    assert res.status_code == 422
