# -*- coding: utf-8 -*-
"""documents/admin.py - 管理画面定義.

Why: 文書とチャンクを目視確認できるようにするため。
What: DocumentとDocumentChunkの管理表示を提供する。
Assumption / Dependencies: Django admin。
I/O: 入力=管理画面操作、出力=DB行。
Caution: なし。
Future Work: なし。
Change Log: 初版作成。
"""

from django.contrib import admin

from documents.models import Document, DocumentChunk


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """文書の管理表示。"""

    list_display = ["id", "title", "updated_at"]


@admin.register(DocumentChunk)
class DocumentChunkAdmin(admin.ModelAdmin):
    """チャンクの管理表示。"""

    list_display = ["id", "document_id", "chunk_index"]
