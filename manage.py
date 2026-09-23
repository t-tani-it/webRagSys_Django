#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""manage.py - Django管理コマンド起動点.

Why: マイグレーションと開発サーバ起動を一元化するため。
What: DJANGO_SETTINGS_MODULEを指定してDjangoを実行する。
Assumption / Dependencies: Django、ragproject.settings。
I/O: 入力=コマンド行引数、出力=コマンド実行結果。
Caution: なし。
Future Work: なし。
Change Log: 初版作成。
"""

import os
import sys


def main() -> None:
    """管理コマンドを実行する。"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ragproject.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django未導入。pip install -r requirements.txtを実行すること") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
