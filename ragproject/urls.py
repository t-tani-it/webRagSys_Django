# -*- coding: utf-8 -*-
"""ragproject/urls.py - URL振分.

Why: 受付点を一元化し、参考と同じ経路を提供するため。
What: health、documents、chat、OpenAPI操作画面を登録する。
Assumption / Dependencies: documents.urls、chat.urls、drf-spectacular。
I/O: 入力=HTTPパス、出力=対応view。
Caution: 末尾スラッシュなし経路で登録する（APPEND_SLASH=Falseと対）。
Future Work: 管理画面URLの追加。
Change Log: 初版作成。
"""

from django.http import JsonResponse
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


def health(_request):  # type: ignore[no-untyped-def]
    """疎通確認用。

    Returns:
        JsonResponse: {"status": "ok"}。
    """
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health", health, name="health"),
    path("documents", include("documents.urls")),
    path("chat", include("chat.urls")),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
