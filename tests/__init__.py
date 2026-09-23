# -*- coding: utf-8 -*-
"""tests - pytestテスト格納.

Why: 文書CRUDとチャットの動作を保証するため。
What: test_documents、test_chatを提供する。
Assumption / Dependencies: pytest、pytest-django（偽実装のため外部通信なし）。
I/O: 入力=APIリクエスト、出力=検証結果。
Caution: DB利用テストにはdjango_dbマークを付けること。
Future Work: 異常系の追加。
Change Log: 初版作成。
"""
