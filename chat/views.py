# -*- coding: utf-8 -*-
"""chat/views.py - AIチャットAPI.

Why: 質問に対してRAG回答を返すため。
What: POST /chatを提供する。
Assumption / Dependencies: DRF、RAG chain。
I/O: 入力=質問JSON、出力=回答JSON。
Caution: DB／LLM障害時は500で返す。
Future Work: 会話履歴対応。
Change Log: 初版作成。
"""

import logging

from django.db import DatabaseError
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from chat.serializers import ChatRequestSerializer, ChatResponseSerializer
from rag.chain import answer_question

logger = logging.getLogger(__name__)


def validate_input(question: str) -> None:
    """入力チェックを行う。

    Args:
        question: 質問文。

    Raises:
        ValueError: 空文字の場合。
    """
    if not question.strip():
        raise ValueError("questionは必須です")


def execute_logic(question: str) -> tuple[str, list[int]]:
    """RAG回答の本体処理。

    Args:
        question: 質問文。

    Returns:
        tuple[str, list[int]]: 回答文と参照文書ID一覧。
    """
    return answer_question(question)


def format_output(answer: str, source_ids: list[int]) -> dict:
    """回答をレスポンス用dictに整形する。

    Args:
        answer: 回答文。
        source_ids: 参照文書ID一覧。

    Returns:
        dict: レスポンス内容。
    """
    serializer = ChatResponseSerializer({"answer": answer, "source_ids": source_ids})
    return dict(serializer.data)


@api_view(["POST"])
def chat(request: Request) -> Response:
    """質問に回答する。

    Args:
        request: HTTPリクエスト。

    Returns:
        Response: 回答と参照ID。
    """
    serializer = ChatRequestSerializer(data=request.data)
    # 解説：検証失敗は例外ハンドラで422に変換される。
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data or {}
    question = str(data["question"])
    validate_input(question)
    try:
        answer, source_ids = execute_logic(question)
    except RuntimeError as exc:
        return Response({"detail": str(exc)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except (DatabaseError, ValueError, OSError) as exc:
        # 解説：DB障害・不正値・入出力障害は500にまとめ、詳細はログに残す。
        logger.warning("chat failed: %s", exc)
        return Response(
            {"detail": "回答生成に失敗しました"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
    return Response(format_output(answer, source_ids))
