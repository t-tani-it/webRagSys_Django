# -*- coding: utf-8 -*-
"""ragproject/settings.py - Django設定.

Why: 受付・保存・操作画面の設定を1か所に集めるため。
What: アプリ登録、SQLite、DRF、OpenAPI、末尾スラッシュ無効化を定義する。
Assumption / Dependencies: config.py（.env読込）、Django、DRF、drf-spectacular。
I/O: 入力=.env、出力=設定値。
Caution: SECRET_KEY既定値は学習用。本番では.envで必ず置換すること。
Future Work: 環境別設定分割、PostgreSQL切替。
Change Log: 初版作成。
"""

from pathlib import Path

from config import get_settings

settings = get_settings()

# 設定値ブロック（冒頭集約）
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = settings.secret_key
DEBUG = settings.debug
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "documents",
    "chat",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ragproject.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ragproject.wsgi.application"

# 解説：正規運用はSQLiteとする。PostgreSQLは構成見本のみで切替は行わない。
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS: list[dict[str, str]] = []

LANGUAGE_CODE = "ja"
TIME_ZONE = "Asia/Tokyo"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# 解説：参考のcurl互換のため末尾スラッシュ付加を無効化する。
APPEND_SLASH = False

REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    # 解説：検証エラー400を422に変換する自前ハンドラを指定する。
    "EXCEPTION_HANDLER": "ragproject.exceptions.compat_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "webRagSys_Django 社内文書検索・AIチャット",
    "DESCRIPTION": (
        "操作順：1 生存確認（GET /health）→ 2 文書登録（POST /documents）"
        "→ 3 質問（POST /chat）。先に登録しないと根拠（source_ids）が空になる。"
    ),
    "VERSION": "1.0.0",
}
