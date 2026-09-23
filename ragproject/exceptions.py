# -*- coding: utf-8 -*-
"""ragproject/exceptions.py - DRF例外の互換変換.

Why: 参考（webRagSys）の422振る舞いをDRFで再現するため。
What: 検証エラー400を422に変換するハンドラを提供する。
Assumption / Dependencies: DRF。
I/O: 入力=例外コンテキスト、出力=ResponseまたはNone。
Caution: 404・500は変換しない。
Future Work: なし。
Change Log: 初版作成。
"""

from typing import Any

from rest_framework.response import Response
from rest_framework.views import exception_handler


def compat_exception_handler(exc: Exception, context: dict[str, Any]) -> Response | None:
    """DRF例外を参考互換に変換する。

    Args:
        exc: 発生した例外。
        context: DRFが渡す実行コンテキスト。

    Returns:
        Response | None: 変換後レスポンス。非DRF例外時はNone。
    """
    # 解説：DRF既定の400（検証失敗・不正JSON）を参考の422に寄せる。
    response = exception_handler(exc, context)
    if response is not None and response.status_code == 400:
        response.status_code = 422
    return response
