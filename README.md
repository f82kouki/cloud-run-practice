# ScoutConnect - 就活スカウトプラットフォーム

Cloud Run デプロイを想定した練習用モノリポ。企業側のスカウト管理画面をモックデータで再現。

## 技術スタック

| 層 | 技術 |
|---|---|
| バックエンド | Python 3.11 / FastAPI / Uvicorn |
| フロントエンド | React 19 / TypeScript / Tailwind CSS / Vite |
| コンテナ | Docker（マルチステージビルド対応） |
| パッケージ管理 | uv（backend）/ npm（frontend） |

## ディレクトリ構成

```
.
├── backend/
│   ├── main.py              # エントリポイント（JOB_TYPE で server/job 切替）
│   ├── app/
│   │   ├── __init__.py      # FastAPI アプリ定義
│   │   ├── models.py        # Pydantic モデル
│   │   └── routers/
│   │       ├── health.py    # GET /health
│   │       ├── dashboard.py # GET /api/dashboard
│   │       ├── students.py  # GET /api/students
│   │       └── scouts.py    # GET /api/scouts
│   ├── jobs/
│   │   └── runner.py        # Cloud Run Jobs 用バッチ処理
│   ├── Dockerfile           # 開発用（--reload あり）
│   └── Dockerfile.prod      # 本番用（マルチステージ）
├── frontend/
│   ├── src/
│   │   ├── App.tsx          # メインアプリ（3タブ構成）
│   │   ├── types.ts         # 型定義
│   │   └── components/
│   │       ├── DashboardStats.tsx
│   │       ├── StudentCard.tsx
│   │       └── ScoutList.tsx
│   └── vite.config.ts       # API プロキシ設定
├── docker-compose.yml
└── Makefile
```

## セットアップ

```bash
# ローカル起動（Docker 必須）
make dev

# 停止
make down
```

- フロントエンド: http://localhost:5176
- バックエンド API: http://localhost:8082

## API エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック |
| GET | `/api/dashboard` | ダッシュボード統計 |
| GET | `/api/students` | 学生一覧（`?industry=` `?graduation_year=` フィルタ対応） |
| GET | `/api/scouts` | スカウト一覧（`?status=` フィルタ対応） |

## Cloud Run Jobs

`JOB_TYPE` 環境変数を指定するとバッチジョブモードで起動:

```bash
# 例: スカウトメール一括送信
make job JOB_TYPE=scout-email-sender
```

対応ジョブ: `scout-email-sender` / `student-data-sync` / `matching-score-calculator` / `weekly-report-generator` / `inactive-student-cleanup` / `scout-reminder-sender`

## 本番イメージビルド

```bash
make build-prod
```

## Make コマンド一覧

| コマンド | 説明 |
|---|---|
| `make dev` | Docker Compose でローカル起動 |
| `make down` | コンテナ停止 |
| `make build` | イメージビルド |
| `make build-prod` | 本番用イメージビルド |
| `make logs` | ログ表示 |
| `make health` | ヘルスチェック実行 |
| `make job JOB_TYPE=xxx` | ジョブ実行 |
