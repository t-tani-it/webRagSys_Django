# -*- coding: utf-8 -*-
"""documents/urls.py - 文書URL振分.

Why: 参考と同じ経路（末尾スラッシュなし）を提供するため。
What: 一覧・登録・詳細・更新・削除の経路を登録する。
Assumption / Dependencies: documents.views。
I/O: 入力=HTTPパス、出力=対応view。
Caution: 親urls.py側で"documents"接頭辞が付く。
Future Work: なし。
Change Log: 初版作成。
"""

from django.urls import path

from documents import views

urlpatterns = [
    path("", views.document_list_create, name="document-list-create"),
    path("/<int:doc_id>", views.document_detail, name="document-detail"),
]
