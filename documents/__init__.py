# -*- coding: utf-8 -*-
"""documents - 文書CRUDアプリ.

Why: 文書管理機能を1アプリにまとめるため。
What: models、serializers、views、urls、adminを提供する。
Assumption / Dependencies: Django、DRF。
I/O: 入力=HTTP／Python属性、出力=JSON／DB行。
Caution: 登録・更新時はチャンク再生成、削除時はチャンク削除を行う。
Future Work: ページング、カテゴリ絞込。
Change Log: 初版作成。
"""
