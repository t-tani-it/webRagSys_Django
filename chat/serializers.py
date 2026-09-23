# -*- coding: utf-8 -*-
"""chat/serializers.py - チャットAPIの入出力定義.

Why: 質問と回答の形式を固定するため。
What: ChatRequest、ChatResponseを提供する。
Assumption / Dependencies: DRF。
I/O: 入力=質問JSON、出力=回答JSON。
Caution: 空質問は422にする（例外ハンドラで400→422変換）。
Future Work: 会話履歴ID、出典スコア追加。
Change Log: 初版作成。
"""

from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    """質問リクエスト。"""

    # 解説：項目名は英語維持し、説明文だけ日本語化して互換性を保つ。
    question = serializers.CharField(
        min_length=1,
        help_text="質問文。1文字以上。空は422。先に文書登録が必要。",
    )

    def validate_question(self, value: str) -> str:
        """質問の空白入力を拒否する。

        Args:
            value: 入力質問。

        Returns:
            str: 検証済み質問。
        """
        # 解説：min_lengthだけでは空白文字列を通すため、strip判定を追加する。
        if not value.strip():
            raise serializers.ValidationError("questionは必須です")
        return value


class ChatResponseSerializer(serializers.Serializer):
    """回答レスポンス。"""

    answer = serializers.CharField(help_text="回答文。根拠なしの場合もある。")
    source_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="根拠文書の番号一覧。空は未登録で質問した状態。",
    )
