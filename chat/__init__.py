# -*- coding: utf-8 -*-
"""chat - AIチャットアプリ.

Why: 質問に対してRAG回答を返す機能を1アプリにまとめるため。
What: serializers、views、urlsを提供する。
Assumption / Dependencies: DRF、rag.chain。
I/O: 入力=質問JSON、出力=回答JSON。
Caution: DB／LLM障害時は500で返す。
Future Work: 会話履歴対応。
Change Log: 初版作成。
"""
