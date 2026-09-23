# webRagSys_Django — 社内文書検索・AIチャットシステム（Django版）

社内文書を登録・管理し、ユーザーからの質問に対して登録文書を検索したうえで生成AIが回答するWeb APIシステム。
webRagSys（FastAPI版）と同等の目的・APIを、可能な限りDjangoで構築する。

## 結論

受付と保存だけをDjangoに置き換える。分割・ベクトル化・検索・回答の順序（RAGの中身）は参考どおりLangChainのままにする。
APIの経路と振る舞いは参考と同じにし、参考のcurlがそのまま動くことを目指す。

## 理由

処理の本質は次の順である。

1. Pythonで処理を書く
2. APIが受付する
3. DBに保存する
4. LLMが文章を作る
5. RAGが「検索してから回答する」

Djangoが担えるのは2と3である。4と5にDjangoの相当機能はないため、参考と同じくLangChainの薄い層で担う。
既定は課金なしの偽実装とし、本番だけ外部APIを使う点も参考と同じである。

## 置き換え

| 参考（webRagSys） | Django版 | 備考 |
|---|---|---|
| FastAPI | Django＋Django REST Framework | 受付と振分を担う |
| Pydanticスキーマ | DRFのSerializer | 入出力の検品を担う |
| SQLAlchemy | Django ORM | 保存と読出を担う |
| uvicorn | `python manage.py runserver` | 起動サーバ |
| `/docs`（Swagger UI） | drf-spectacularのSwagger UI | 操作画面。`/api/docs/`で提供する |
| LangChain | そのまま移植 | TextSplitter利用。分割・検索・回答の順序は自前層 |
| SQLiteが正規 | 同じ（`db.sqlite3`） | PostgreSQL＋pgvectorは構成見本のみ |
| Docker検証 | 対象外。ファイルだけ残す | 参考と同じ方針 |

APIは同じである。`GET /health`、文書の一覧・詳細・登録・更新・削除、`POST /chat`である。
登録・更新の直後にチャンクを作り直し、削除時はチャンクも消す。
存在しないIDは404、空入力は422、チャット障害は500である。

## 作るもの

```text
webRagSys_Django/
├── manage.py
├── config.py              ← 設定集約（.env読込。キーは直書きしない）
├── requirements.txt
├── .env.example           ← 既定は USE_FAKE=true
├── ragproject/            ← Django本体（settings、urls、例外ハンドラ）
├── documents/             ← 文書CRUD（models、serializers、views、urls、admin）
├── chat/                  ← 質問API（serializers、views、urls）
├── rag/                   ← chunker、embeddings、vectorstore、chain
├── llm/                   ← provider.py（切替）、fake_provider.py（偽回答）
├── tests/                 ← test_documents.py、test_chat.py
├── docs/                  ← handover.md、beginner_overview.md（テスト後）
└── diagrams/              ← Mermaid図（テスト後）
```

RAGの中身は参考の薄い層を移植する。本文をLangChainのTextSplitterで分割し、既定は偽ベクトル、
類似検索はコサイン、`chain`は検索してから回答する順序だけを決める。LCELへの作り替えはしない。

## 変えないもの

- APIの経路とJSONの項目名（`title`、`content`、`question`、`answer`、`source_ids`）
- 偽実装既定（`USE_FAKE=true`、テストは外部通信なし）
- SQLite正規運用、Dockerは構成見本のみ
- 設定値の集約先（`config.py`、値は`chunk_size=500`、`chunk_overlap=50`、`top_k=3`）

## セットアップ方法

```bash
# 0. プロジェクト直下へ移動
cd <プロジェクト直下>

# 1. 仮想環境作成・有効化（venv標準）
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# 2. 依存導入
pip install -r requirements.txt

# 3. 環境変数ファイル作成（公開用見本から複製）
copy .env.example .env

# 4. .env編集（偽実装のままならキー不要）
# USE_FAKE=true
# 本番のみ以下を設定
# OPENAI_API_KEY=xxxx
# USE_FAKE=false

# 5. マイグレーション
python manage.py migrate
```

## 起動方法

```bash
# .venv有効化が前提（プロンプトに(.venv)表示を確認）
.\.venv\Scripts\Activate.ps1

# ローカル起動（正規の動作確認手段）
python manage.py runserver
```

Docker起動は対象外とする。Dockerfileとdocker-compose.ymlは構成見本として残す。

## 動作確認

- http://127.0.0.1:8000/health → `{"status":"ok"}`表示で生存確定
- http://127.0.0.1:8000/api/docs/ → 操作画面表示
- http://127.0.0.1:8000/documents → 初期は`[]`表示で正常

## API一覧

| メソッド | エンドポイント | 内容 |
|----------|---------------|------|
| GET | /health | 生存確認 |
| GET | /documents | 文書一覧取得 |
| GET | /documents/{id} | 文書詳細取得 |
| POST | /documents | 文書登録 |
| PUT | /documents/{id} | 文書更新 |
| DELETE | /documents/{id} | 文書削除 |
| POST | /chat | AIチャット |

リクエスト／レスポンスはJSONを使用する。末尾スラッシュなしで受け付ける。

## RAGの処理概要

```text
文書
 ↓
テキスト分割（LangChain TextSplitter）
 ↓
Embedding（本番：外部API／既定：Fake）
 ↓
Vector Databaseへ保存（DocumentChunk、embeddingはJSON列）

ユーザー質問
 ↓
Embedding
 ↓
類似文書検索（Python側コサイン計算）
 ↓
検索結果をコンテキスト化
 ↓
LLM（本番：外部API／既定：Fake LLM）
 ↓
回答（＋参照文書ID）
```

## 使用方法

```bash
# 文書登録例
curl -X POST http://localhost:8000/documents ^
  -H "Content-Type: application/json" ^
  -d "{\"title\": \"休暇規定\", \"content\": \"年次休暇は...\"}"

# 質問例
curl -X POST http://localhost:8000/chat ^
  -H "Content-Type: application/json" ^
  -d "{\"question\": \"休暇申請の手順は？\"}"
```

## テスト方法

```bash
# 全テスト（偽実装のため外部通信なし）
python -m pytest tests -q

# Lint
python -m ruff check .
```

テスト内容：
- 文書：登録、取得、更新、削除、存在しないIDのエラー、空入力のエラー
- チャット：質問送信、偽LLM回答、登録文書利用、空質問のエラー

## ドキュメント

- `docs/handover.md`：進捗管理（方針→実装→結果→残タスク→実行コマンド）
- `docs/beginner_overview.md`：初心者向け解説（テスト後に作成）
- `diagrams/`：フローチャート、シーケンス、クラス、マインドマップ、状態遷移（テスト後に作成）

## 今後の拡張案

- ユーザー認証、文書ファイルアップロード、PDF／Word対応
- 文書カテゴリ管理、会話履歴、回答の出典表示
- Webフロントエンド、クラウドデプロイ、CI/CD
- 高度なRAG検索、AIエージェント機能

## 完成条件（初期版）

1. runserver起動、文書CRUD動作（ローカル起動で確認、DBはSQLite）
2. LLM API利用可（本番）／偽実装動作（既定）
3. Embedding化、Vector保存、類似検索、RAG回答
4. 基本テスト実行、ruffエラー0
5. Docker構築は対象外

## 注意点

- `.env`はGit管理対象外。APIキー等を公開しないこと
- Djangoは既定でURL末尾スラッシュを付ける癖がある。本件では`APPEND_SLASH=False`とし参考のcurl互換を保つ
- DRFの入力エラーは既定で400になる。本件では例外ハンドラで422に変換する
- docsとdiagramsはテストの後に作成し、作成前に方針を確認すること
