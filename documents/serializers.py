# -*- coding: utf-8 -*-
"""documents/serializers.py - 文書APIの入出力定義.

Why: リクエスト検証とレスポンス整形を分離するため。
What: 作成・更新・参照シリアライザを提供する。
Assumption / Dependencies: DRF。
I/O: 入力=JSON、出力=検証済みdict。
Caution: 空文字は422にする（例外ハンドラで400→422変換）。
Future Work: カテゴリ追加。
Change Log: 初版作成。
"""

from typing import Any

from rest_framework import serializers

from documents.models import Document


def _must_not_be_blank(value: str, field_name: str) -> str:
    """空白のみの入力を拒否する。

    Args:
        value: 入力値。
        field_name: 項目名（エラー文用）。

    Returns:
        str: 検証済み値。

    Raises:
        serializers.ValidationError: 空白のみの場合。
    """
    # 解説：min_lengthだけでは空白文字列を通すため、strip判定を追加する。
    if not value.strip():
        raise serializers.ValidationError(f"{field_name}は必須です")
    return value


class DocumentWriteSerializer(serializers.Serializer):
    """文書登録・更新リクエスト。"""

    # 解説：項目名は英語維持し、説明文だけ日本語化して互換性を保つ。
    title = serializers.CharField(
        min_length=1,
        max_length=200,
        help_text="文書題名。1文字以上200文字以下。空は422。",
    )
    content = serializers.CharField(
        min_length=1,
        help_text="文書本文。1文字以上。検索と回答の根拠になる。",
    )

    def validate_title(self, value: str) -> str:
        """題名の空白入力を拒否する。

        Args:
            value: 入力題名。

        Returns:
            str: 検証済み題名。
        """
        return _must_not_be_blank(value, "title")

    def validate_content(self, value: str) -> str:
        """本文の空白入力を拒否する。

        Args:
            value: 入力本文。

        Returns:
            str: 検証済み本文。
        """
        return _must_not_be_blank(value, "content")


class DocumentOutSerializer(serializers.ModelSerializer):
    """文書レスポンス。"""

    class Meta:
        """対象モデルと出力項目。"""

        model = Document
        fields: Any = ["id", "title", "content", "created_at", "updated_at"]
        read_only_fields: Any = ["id", "created_at", "updated_at"]
