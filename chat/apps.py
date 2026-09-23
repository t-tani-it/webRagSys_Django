# -*- coding: utf-8 -*-
"""chat/apps.py - アプリ定義.

Why: Djangoにチャットアプリを登録するため。
What: ChatConfigを提供する。
Assumption / Dependencies: Django。
I/O: 入力=なし、出力=アプリ設定。
Caution: なし。
Future Work: なし。
Change Log: 初版作成.
"""

from django.apps import AppConfig


class ChatConfig(AppConfig):
    """チャットアプリ設定。"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "chat"
