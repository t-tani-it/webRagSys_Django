# -*- coding: utf-8 -*-
"""ragproject/wsgi.py - WSGI起動点.

Why: 本番サーバから起動できるようにするため。
What: WSGIアプリケーションを提供する。
Assumption / Dependencies: Django。
I/O: 入力=WSGIリクエスト、出力=WSGIレスポンス。
Caution: なし。
Future Work: なし。
Change Log: 初版作成。
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ragproject.settings")

application = get_wsgi_application()
