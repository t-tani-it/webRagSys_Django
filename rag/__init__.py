# -*- coding: utf-8 -*-
"""rag - RAG処理パッケージ.

Why: 分割・検索・回答組立をAPI層から分離するため。
What: chunker、embeddings、vectorstore、chainを提供する。
Assumption / Dependencies: LangChain（TextSplitter）、Django ORM。
I/O: 入力=文書本文・質問文、出力=チャンク・回答。
Caution: 既定は課金なしFake。本番のみ外部通信する。
Future Work: LCEL Chainへの置換、出典スコア付与。
Change Log: 初版作成。
"""
