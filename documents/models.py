# -*- coding: utf-8 -*-
"""documents/models.py - 文書テーブル定義.

Why: 文書とRAG用チャンクの保存先を定義するため。
What: Document、DocumentChunkを提供する。
Assumption / Dependencies: Django ORM。
I/O: 入力=Python属性、出力=DB行。
Caution: embedding列はJSON代替とする（SQLite正規のため）。
Future Work: カテゴリ・会話履歴テーブル追加。
Change Log: 初版作成。
"""

from django.db import models


class Document(models.Model):
    """文書テーブル。"""

    # 解説：項目名は参考と合わせ、検索と回答の根拠になる本文を持つ。
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """テーブル付加情報。"""

        ordering = ["id"]

    def __str__(self) -> str:
        """管理画面表示用。

        Returns:
            str: 文書題名。
        """
        return self.title


class DocumentChunk(models.Model):
    """RAG検索用チャンクテーブル。"""

    # 解説：文書削除時はチャンクも連鎖削除し、古いベクトルを残さない。
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    chunk_index = models.IntegerField()
    content = models.TextField()
    embedding = models.JSONField(default=list)

    class Meta:
        """テーブル付加情報。"""

        ordering = ["document_id", "chunk_index"]

    def __str__(self) -> str:
        """管理画面表示用。

        Returns:
            str: 文書IDと枝番。
        """
        return f"doc={self.document_id} chunk={self.chunk_index}"
