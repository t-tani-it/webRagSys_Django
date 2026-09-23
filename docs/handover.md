# docs/handover.md - webRagSys_Django 進捗管理

本ファイルは進捗管理用mdである。フェーズ完了ごとに更新する。
形式：方針（計画）→実装（実行）→結果→残タスク→実行コマンド。
人間とAIの双方がコンテキスト0%から再開できる粒度で相当詳しく記録する。

---

## 初期化フェーズ（README＋進捗管理先行）

### 方針（計画）
- 対象フォルダ：webRagSys_Django（親フォルダの兄弟フォルダ。他フォルダは読込不要）
- 目的はwebRagSysと同様。社内文書CRUD＋RAG＋AIチャットを可能な限りDjangoで構築する
- 参考の確認事項：
  - 参考（webRagSys）はLangChainを使用している。RAGフレームワークはLangChain固定とする
  - 処理の本質：Python → API → DB → LLM → RAG
  - 技術選定の確定事項：
    - 受付と保存だけDjangoに置き換える（Django＋DRF＋Django ORM）
    - RAGの中身（分割・ベクトル化・検索・回答の順序）はLangChainのまま移植する
    - LLM／Embedding：既定は課金回避の偽実装、本番のみ外部LLM API
    - DB方針：SQLite正規。PostgreSQL＋pgvectorは構成見本のみ
    - 操作画面：drf-spectacularのSwagger UI（`/api/docs/`）
  - API互換の確定事項：
    - 経路は参考と同じ（`/health`、文書CRUD、POST `/chat`、末尾スラッシュなし）
    - 存在しないIDは404、空入力は422、チャット障害は500
    - DRF既定の400は例外ハンドラで422に変換する
    - 登録・更新直後にチャンク再生成、削除時はチャンクも削除する
- 順序の指定：
  - docs（beginner_overview等）とdiagramsはテストの後に作成し、作成前に方針を確認する
  - READMEと進捗管理用mdは先行作成する
  - READMEには理由・置き換え・作るものを独立した節として含める
- AGENTS.mdは親フォルダのマスタAGENTS.mdを継承し、内容に従う
- PDFはmdファイルと同内容のため読み込み不要（参照時の指定）
- セキュリティ：ローカルパス、APIキー、個人ID、認証情報は一切記録しない。機密情報は.env（Git除外）のみ
- 依存の実測：
  - Python 3.11.15、Django 5.2.17、djangorestframework 3.18.1、drf-spectacular 0.30.0
  - langchain_text_splitters 1.1.2（langchain-core 1.6.4を伴う）
  - pytest 9.1.1、pytest-django 4.14.0、python-dotenv 1.2.3、ruff 0.16.8

### 実装（実行）
- webRagSys_Djangoフォルダの空を確認（True、子なし）
- `.venv`をプロジェクト直下に作成（`python -m venv .venv`、Python 3.11.15を確認）
- 依存を導入（django、djangorestframework、drf-spectacular、langchain_text_splitters、python-dotenv、pytest、pytest-django、ruff）
- webRagSys_Django/AGENTS.md作成（Django＋DRF＋SQLite＋偽実装既定＋API互換ルールを固有化）
- webRagSys_Django/README.md作成（結論・理由・置き換え・作るもの・変えないものを独立節として含む）
- 本handover.md作成（本ファイル）

### 結果
- 3ファイル生成完了：
  - webRagSys_Django/AGENTS.md
  - webRagSys_Django/README.md
  - webRagSys_Django/docs/handover.md
- 単体テスト：未実施（実装なしのため）
- Lint：未実施（実装なしのため）

### 残タスク
- [ ] 骨格実装：config.py、requirements.txt、.env.example、.gitignore、pyproject.toml、manage.py、ragproject
- [ ] 文書CRUD実装：documentsアプリ（models、serializers、views、urls、admin）
- [ ] RAG実装：rag（chunker、embeddings、vectorstore、chain）、llm（provider、fake_provider）
- [ ] chat実装：chatアプリ（POST /chat、検索→プロンプト組立→LLM呼出→回答＋参照ID）
- [ ] テスト実装＋実行：pytest全件成功、ruffエラー0（docs着手条件）
- [ ] 起動検証：runserver＋SQLiteでhealth／CRUD／chatを実HTTP確認
- [ ] docs本格作成（テスト後、作成前に方針確認）：beginner_overview.md、README追記
- [ ] diagrams作成（テスト後、作成前に方針確認）：6種（.mmd＋.md＋.pdf）
- [ ] GitHub公開：public、分割コミット、push前禁止情報チェック（明示依頼があるまで行わない）

### 実行コマンド
```powershell
# 環境確認（実施済み）
python --version
.\.venv\Scripts\python.exe --version

# 依存導入（実施済み）
.\.venv\Scripts\pip.exe install "django>=5,<6" "djangorestframework>=3.15" "drf-spectacular>=0.27" "langchain_text_splitters>=0.2" "python-dotenv>=1.0" "pytest>=8.0" "pytest-django>=4.8" "ruff>=0.4"

# 今後のテスト／Lint（予定）
python -m pytest tests -q
python -m ruff check .

# 今後の起動（予定）
python manage.py migrate
python manage.py runserver
```

### 実行成果物
- webRagSys_Django/AGENTS.md
- webRagSys_Django/README.md
- webRagSys_Django/docs/handover.md

## 公開禁止情報
公開禁止情報は含まれていません

---

## 実装フェーズ（骨格＋CRUD＋RAG＋chat＋テスト）

### 方針（計画）
- 先行作成済みのAGENTS.md、README.mdに従い、参考（webRagSys）と同等のAPIをDjangoで再現する
- 受付と保存だけDjangoに置き換える。RAGの中身はLangChainのまま薄い層で移植する
- 既定USE_FAKE=trueで課金なし。EmbeddingはFakeベクトル、LLMはFake定型文
- DBはSQLite正規。PostgreSQL＋pgvectorは構成見本のみ
- docsとdiagramsはテストの後に作り、作成前に方針を確認する指定のため、本フェーズでは作らない

### 実装（実行）
- 骨格：requirements.txt、config.py（Settings集約）、.env.example、.gitignore、pyproject.toml、manage.py、ragproject（settings、urls、exceptions、wsgi、asgi）、Dockerfile、docker-compose.yml（構成見本）
- 文書：documentsアプリ（models Document／DocumentChunk、serializers、views、urls、admin、migration 0001）
- RAG：rag/chunker.py（LangChain優先＋単純分割退避）、rag/embeddings.py（Fake既定／OpenAI本番）、rag/vectorstore.py（ORM置換保存／削除／コサイン検索）、rag/chain.py（answer_question）
- LLM：llm/fake_provider.py、llm/provider.py（USE_FAKE切替）
- API：ragproject/urls.py（health、documents、chat、api/schema、api/docs）、documents/views.py（CRUD、一覧・詳細・登録・更新・削除、登録更新時にchunks再生成、削除時にchunks削除）、chat/views.py（POST /chat、500処理）
- 互換：APPEND_SLASH=Falseで末尾スラッシュなし受付、例外ハンドラで検証エラー400を422に変換
- テスト：tests/test_documents.py（7件）、tests/test_chat.py（3件）、pytest-django利用
- 修正：
  - ruffでS101（assert）→validated_data or {}に変更
  - ruffでBLE001（broad-except）→DatabaseError／ValueError／OSErrorに限定＋ログ記録
  - ruffでRUF012（Django定石の可変クラス属性）→該当ファイルで除外設定
  - ruffでRET501（return None）→healthのvalidate層を除去して単純化
  - ruff formatで9件整形

### 結果
- 単体テスト：10件すべて成功（python -m pytest tests -q）
- Lint：ruffエラー0（python -m ruff check . → All checks passed）
- 実HTTP検証（port 8001、起動→検証→停止）：
  - GET /health → ok
  - POST /documents → id付きで作成（201）
  - GET /documents → 一覧取得
  - GET /documents/2 → 詳細取得
  - POST /chat → FAKE回答＋source_ids取得
  - GET /documents/99999 → 404
  - 空題名POST → 422、空質問POST → 422
  - GET /api/docs → 200、GET /api/schema → 200
- 検証後にdb.sqlite3を削除（実行生成物のため）
- PDF：未生成（テスト後工程のため）

### 残タスク
- [ ] docs本格作成（テスト後、作成前に方針確認）：beginner_overview.md、README追記
- [ ] diagrams作成（テスト後、作成前に方針確認）：6種（.mmd＋.md＋.pdf）
- [ ] PDF生成：docs PDF、diagrams PDF
- [ ] GitHub公開：public、分割コミット、push前禁止情報チェック（明示依頼があるまで行わない）

### 実行コマンド
```powershell
# 依存
pip install -r requirements.txt
# マイグレーション
python manage.py migrate
# テスト／Lint
python -m pytest tests -q
python -m ruff check .
# 起動
python manage.py runserver
```

### 実行成果物
- config.py、requirements.txt、pyproject.toml、manage.py、Dockerfile、docker-compose.yml、.env.example、.gitignore
- ragproject一式、documents一式、chat一式、rag一式、llm一式
- tests/test_documents.py、tests/test_chat.py
- README.md（完成条件・テスト節の実績反映は次回更新時に行う）

## 公開禁止情報
公開禁止情報は含まれていません

---

## GitHub公開フェーズ

### 方針（計画）
- publicリポジトリで公開し、履歴が読める分割コミットにする
- push前に公開禁止情報（.env、実パス、キー）をチェックする

### 実装（実行）
- 状態確認：.envなし、db.sqlite3なし（検証後に削除済み）、.venvは.gitignoreで除外を確認
- 禁止情報検査：追跡対象は例示プレースホルダ（`C:\Users\...`、`OPENAI_API_KEY=xxxx`）のみで実情報なし
- git init -b main、user.nameとuser.emailをリポジトリローカルに設定（noreply形式）
- 分割コミット5件：
  - 骨格・設定・Docker基盤・README・handover先行作成
  - Django本体・文書CRUD
  - RAG・LLM偽実装
  - chat API
  - テスト
- gh repo create webRagSys_Django --public --source . --remote originで作成
- git push -u origin mainで公開

### 結果
- 公開先：https://github.com/t-tani-it/webRagSys_Django
- mainがorigin/mainを追跡する状態を確認
- git statusはクリーン

### 残タスク
- [x] docs本格作成：beginner_overview.md（下記フェーズで実施）
- [x] diagrams作成：6種（下記フェーズで実施）
- [x] PDF生成：docs PDF、diagrams PDF（下記フェーズで実施）
- [ ] GitHub公開分の追加commit＋push（本フェーズ成果物）

### 実行コマンド
```powershell
git log --oneline
git push -u origin main
```

### 実行成果物
- docs/handover.md（本ファイル）

## 公開禁止情報
公開禁止情報は含まれていません

---

## ドキュメント・図フェーズ（初心者文書と図6種）

### 方針（計画）
- 初心者文書は参考より詳しく丁寧に書く。対象はPython中級・RAG初心者であり、用語のいきなり出しを避ける
- 文体はである調、表のセルは述語なしとする
- 図は6種（フロー、シーケンス、RAGクラス、モジュールクラス、マインドマップ、状態）とする
- PDFの下側には文書名とページ番号（N / 総数）を付与する
- PDFはmdファイルと同内容のため、PDF自体の読込みは不要である

### 実装（実行）
- docs/beginner_overview.md作成：
  - 0章：読み方と対象、書庫係・索引係・回答係のたとえ
  - 1章：目的と操作7件、なぜDjangoかの置き換え表
  - 2章：用語の事前説明（API、JSON、CRUD、RAG、チャンク、Embedding、ベクトル、LLM、Django用語）
  - 3章：フォルダ構成と主要ファイルの実コード行番号付き対応表
  - 4章：具体例（題名「休暇規定」、本文「年次休暇は10日付与する。」）の登録→RAG化→質問応答トレース、偽ベクトル実数値とコサイン0.7253を記載
  - 5章：更新の全置換と削除の索引先行
  - 6章：Djangoのつまずき点（アプリ、マイグレーション、Serializer、APPEND_SLASH=False、422変換）
  - 7章：LangChainと偽実装のつまずき点（TextSplitterのみ、切替条件、使う使われる関係）
  - 8章：/api/docs/操作と裏側関数の対応、回答と異常の見分け方
  - 付録：学習順番10段階
- diagrams 6種作成（.mmd＋.md）：
  - 01_flowchart：起動→CRUD分岐→RAG化→chat分岐
  - 02_sequence：登録と質問応答の通信
  - 03a_class_rag：Chunker／Embeddings／VectorStore／Chain／LLM
  - 03b_class_modules：Settings／URLs／Views／Model／Serializer／例外変換
  - 04_mindmap：全体概念階層
  - 05_state：PENDING→CHUNKING→EMBEDDING→SAVING→COMPLETED（概念図であり状態列ではない）
- 各図mdは「何を示すか→なぜ必要か→読み方→混乱点→実コード対応→図」の順に記載
- mermaid-cliで6件PNG生成
- 各図mdのmermaidブロックを画像参照＋details（元コード保持）に置換
- md-to-pdfで7件PDF生成（docs 1件＋図6件）。フッターに文書名とページ番号を付与
- PDF検証：pypdfで確認（beginner 6頁、図は1-2頁、図PDF各1画像埋込み、フッター文書名とN / 総数を検出）

### 結果
- 単体テスト：10件すべて成功（python -m pytest tests -q）
- Lint：ruffエラー0
- PDF：7件生成（docs 1件＋図6件）

### 残タスク
- [ ] GitHub公開分の追加commit＋push（本フェーズ成果物）

### 実行コマンド
```powershell
# PNG生成
npx.cmd -y @mermaid-js/mermaid-cli -i diagrams/01_flowchart.mmd -o diagrams/01_flowchart.png
# docs PDF生成（フッター設定付き）
npx md-to-pdf docs/beginner_overview.md --config-file <フッター設定>
# テスト／Lint
python -m pytest tests -q
python -m ruff check .
```

### 実行成果物
- docs/beginner_overview.md＋.pdf
- diagrams 6種（.mmd＋.md＋.png＋.pdf）
- README.md（ドキュメント節更新）
- docs/handover.md（本ファイル）

## 公開禁止情報
公開禁止情報は含まれていません
