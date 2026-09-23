# -*- coding: utf-8 -*-
"""documents/apps.py - アプリ定義.

Why: Djangoに文書アプリを登録するため。
What: DocumentsConfigを提供する。
Assumption / Dependencies: Django。
I/O: 入力=なし、出力=アプリ設定。
Caution: なし。
Future Work: なし。
Change Log: 初版作成.
"""

from django.apps import AppConfig


class DocumentsConfig(AppConfig):
    """文書アプリ設定。"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "documents"
