# -*- coding: utf-8 -*-
"""config.py - webRagSys_Django全体の設定値集約.

Why: 設定値を1か所に集め、環境変数で切替可能にするため。
What: RAG、LLM偽装フラグ、Django起動値を定義する。
Assumption / Dependencies: python-dotenvに依存。
I/O: 入力=.env／環境変数、出力=Settingsインスタンス。
Caution: APIキー等の機密情報を直書きしないこと。
Future Work: 環境別（dev/prod）設定ファイル分割。
Change Log: 初版作成。
"""

import os
from dataclasses import dataclass, field
from functools import lru_cache

from dotenv import load_dotenv

# 解説：起動直後に.envを読込み、環境変数へ反映する。
load_dotenv()


def _get_bool(name: str, default: bool) -> bool:
    """真偽値の環境変数を読み取る。

    Args:
        name: 環境変数名。
        default: 未設定時の値。

    Returns:
        bool: 解釈した真偽値。
    """
    raw = os.getenv(name)
    if raw is None:
        return default
    # 解説：true/1/yes/onを真とみなす。大小文字は区別しない。
    return raw.strip().lower() in ("true", "1", "yes", "on")


def _get_int(name: str, default: int) -> int:
    """整数の環境変数を読み取る。

    Args:
        name: 環境変数名。
        default: 未設定時・不正時の値。

    Returns:
        int: 解釈した整数。
    """
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


# 設定値ブロック（冒頭集約）
@dataclass(frozen=True)
class Settings:
    """アプリケーション設定値。"""

    # アプリ識別
    app_name: str = field(default_factory=lambda: os.getenv("APP_NAME", "webRagSys_Django"))

    # RAG関連の設定値（LangChain用）
    chunk_size: int = field(default_factory=lambda: _get_int("CHUNK_SIZE", 500))
    chunk_overlap: int = field(default_factory=lambda: _get_int("CHUNK_OVERLAP", 50))
    top_k: int = field(default_factory=lambda: _get_int("TOP_K", 3))

    # LLM関連の設定値（偽実装切替）
    use_fake: bool = field(default_factory=lambda: _get_bool("USE_FAKE", True))
    openai_api_key: str = field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    openai_model: str = field(default_factory=lambda: os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    openai_embedding_model: str = field(
        default_factory=lambda: os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    )

    # Django起動関連の設定値
    secret_key: str = field(
        default_factory=lambda: os.getenv(
            "DJANGO_SECRET_KEY", "django-insecure-learning-default-change-in-production"
        )
    )
    debug: bool = field(default_factory=lambda: _get_bool("DJANGO_DEBUG", True))


@lru_cache
def get_settings() -> Settings:
    """設定値シングルトンを返す。

    Returns:
        Settings: 設定値インスタンス。

    Side Effects:
        なし（.env読込はモジュール読込時に済む）。
    """
    return Settings()
