# -*- coding: utf-8 -*-
"""chat/urls.py - チャットURL振分.

Why: 参考と同じ経路（末尾スラッシュなし）を提供するため。
What: POST /chatの経路を登録する。
Assumption / Dependencies: chat.views。
I/O: 入力=HTTPパス、出力=対応view。
Caution: 親urls.py側で"chat"接頭辞が付く。
Future Work: なし。
Change Log: 初版作成。
"""

from django.urls import path

from chat import views

urlpatterns = [
    path("", views.chat, name="chat"),
]
