# -*- coding: utf-8 -*-
"""documents/views.py - 文書CRUD API.

Why: 文書管理機能を提供するため。
What: 一覧・詳細・登録・更新・削除を提供する。
Assumption / Dependencies: DRF、Django ORM、rag層。
I/O: 入力=JSON／パスID、出力=JSON。
Caution: 存在しないIDは404、不正入力は422を返す。
Future Work: ページング、カテゴリ絞込。
Change Log: 初版作成。
"""

from typing import Any

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from documents.models import Document
from documents.serializers import DocumentOutSerializer, DocumentWriteSerializer
from rag import chunker, vectorstore


def validate_input(title: str, content: str) -> None:
    """入力チェックを行う。

    Args:
        title: タイトル。
        content: 本文。

    Raises:
        ValueError: 空文字の場合。
    """
    if not title.strip() or not content.strip():
        raise ValueError("titleとcontentは必須です")


def execute_logic_register(title: str, content: str) -> Document:
    """文書登録の本体処理。

    Args:
        title: 題名。
        content: 本文。

    Returns:
        Document: 登録行。

    Side Effects:
        documents挿入、chunks保存。
    """
    doc = Document.objects.create(title=title, content=content)
    # 解説：RAG検索用に登録直後にチャンク化する。
    vectorstore.save_chunks(doc.id, chunker.split_text(doc.content))
    return doc


def execute_logic_update(doc: Document, title: str, content: str) -> Document:
    """文書更新の本体処理。

    Args:
        doc: 更新対象。
        title: 新題名。
        content: 新本文。

    Returns:
        Document: 更新行。

    Side Effects:
        documents更新、chunks置換。
    """
    doc.title = title
    doc.content = content
    doc.save()
    # 解説：古いベクトルが残らないよう、更新直後にチャンクを作り直す。
    vectorstore.save_chunks(doc.id, chunker.split_text(doc.content))
    return doc


def format_output(doc: Document) -> dict[str, Any]:
    """文書行をレスポンス用dictに整形する。

    Args:
        doc: 文書行。

    Returns:
        dict[str, Any]: レスポンス内容。
    """
    return dict(DocumentOutSerializer(doc).data)


@api_view(["GET", "POST"])
def document_list_create(request: Request) -> Response:
    """文書一覧・登録を処理する。

    Args:
        request: HTTPリクエスト。

    Returns:
        Response: 一覧JSONまたは登録JSON。
    """
    if request.method == "GET":
        # 解説：一覧はRAGを使わない。id順で返す。
        docs = Document.objects.all()
        return Response(DocumentOutSerializer(docs, many=True).data)
    serializer = DocumentWriteSerializer(data=request.data)
    # 解説：検証失敗は例外ハンドラで422に変換される。
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data or {}
    validate_input(str(data["title"]), str(data["content"]))
    doc = execute_logic_register(str(data["title"]), str(data["content"]))
    return Response(format_output(doc), status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def document_detail(request: Request, doc_id: int) -> Response:
    """文書詳細・更新・削除を処理する。

    Args:
        request: HTTPリクエスト。
        doc_id: 文書ID。

    Returns:
        Response: 詳細JSON、更新JSON、または空204。
    """
    # 解説：存在しない番号は404にする。
    doc = get_object_or_404(Document, pk=doc_id)
    if request.method == "GET":
        return Response(format_output(doc))
    if request.method == "PUT":
        serializer = DocumentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data or {}
        validate_input(str(data["title"]), str(data["content"]))
        doc = execute_logic_update(doc, str(data["title"]), str(data["content"]))
        return Response(format_output(doc))
    # 解説：文書削除時はひも付くチャンクも消す（CASCADEに加え明示削除）。
    vectorstore.delete_chunks(doc.id)
    doc.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
