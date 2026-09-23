# -*- coding: utf-8 -*-
"""tests/test_documents.py - 文書CRUDテスト.

Why: 文書の登録・取得・更新・削除を保証するため。
What: 正常系5件＋異常系2件を提供する。
Assumption / Dependencies: pytest-django、DRFテストクライアント。
I/O: 入力=APIリクエスト、出力=検証結果。
Caution: 偽実装のため外部通信しない。
Future Work: ページング追加時の追従。
Change Log: 初版作成。
"""

import pytest
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


def _register(client: APIClient) -> dict:
    """文書を1件登録する。

    Args:
        client: テストクライアント。

    Returns:
        dict: 登録レスポンス。
    """
    res = client.post(
        "/documents",
        {"title": "休暇規定", "content": "年次休暇は10日付与する。"},
        format="json",
    )
    assert res.status_code == 201
    data = res.json()
    assert data["id"] == 1
    return data


def test_register_document() -> None:
    """文書登録ができる。"""
    client = APIClient()
    data = _register(client)
    assert data["title"] == "休暇規定"


def test_list_documents() -> None:
    """文書一覧が取得できる。"""
    client = APIClient()
    _register(client)
    res = client.get("/documents")
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_get_document() -> None:
    """文書詳細が取得できる。"""
    client = APIClient()
    _register(client)
    res = client.get("/documents/1")
    assert res.status_code == 200
    assert res.json()["content"] == "年次休暇は10日付与する。"


def test_update_document() -> None:
    """文書更新ができる。"""
    client = APIClient()
    _register(client)
    res = client.put(
        "/documents/1",
        {"title": "休暇規定改訂", "content": "年次休暇は11日付与する。"},
        format="json",
    )
    assert res.status_code == 200
    assert res.json()["title"] == "休暇規定改訂"


def test_delete_document() -> None:
    """文書削除ができる。"""
    client = APIClient()
    _register(client)
    res = client.delete("/documents/1")
    assert res.status_code == 204
    assert client.get("/documents").json() == []


def test_get_missing_document_returns_404() -> None:
    """存在しないIDは404になる。"""
    client = APIClient()
    res = client.get("/documents/99999")
    assert res.status_code == 404


def test_register_blank_returns_422() -> None:
    """空入力は422になる。"""
    client = APIClient()
    res = client.post("/documents", {"title": " ", "content": "本文"}, format="json")
    assert res.status_code == 422
