# -*- coding: utf-8 -*-
"""llm - LLM呼出パッケージ.

Why: 偽実装と本番APIの切替点を1か所にまとめるため。
What: provider（切替）、fake_provider（偽回答）を提供する。
Assumption / Dependencies: langchain-openaiは本番時のみ必要。
I/O: 入力=質問＋コンテキスト、出力=回答文。
Caution: 既定は課金なしFake。
Future Work: モデル別プロバイダ追加。
Change Log: 初版作成。
"""
