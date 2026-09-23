# -*- coding: utf-8 -*-
"""ragproject/asgi.py - ASGI起動点.

Why: ASGIサーバから起動できるようにするため。
What: ASGIアプリケーションを提供する。
Assumption / Dependencies: Django。
I/O: 入力=ASGIリクエスト、出力=ASGIレスポンス。
Caution: なし。
Future Work: なし。
Change Log: 初版作成。
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ragproject.settings")

application = get_asgi_application()
