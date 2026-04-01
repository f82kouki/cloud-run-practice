# Phase 4: デプロイ & CI/CD 作戦書

## Context

Vimmyモノリスから分離した `vimmy-tools` を独立サービスとしてデプロイするためのインフラ構築。Cloud Run（バックエンド）、Firebase Hosting（フロントエンド）、Cloud Run Jobs（バッチ処理）、Cloud Scheduler（定期実行）、GitHub Actions（CI/CD）を設定する。

**GCPプロジェクト:** `vimmy-459300` / **リージョン:** `asia-northeast1`

### 担当分担
- **Claudeが実装:** Dockerfile.prod、firebase.json、.firebaserc、GitHub Actions 4ワークフロー
- **ユーザーが手動実施:** Cloud Run Jobs作成（4-3）、Cloud Scheduler設定（4-4）、Secret Manager登録、GCPリソース作成

---

## 4-1. 本番用Dockerfile作成

現在の `backend/Dockerfile` は開発用（`--reload`、dev依存）。本番用を作成する。

**作成ファイル:** `backend/Dockerfile.prod`

```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv pip install --system .

FROM python:3.11-slim
WORKDIR /app

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . .

ENV PYTHONPATH=/app
EXPOSE 8081

# main.py がJOB_TYPE有無でサーバー/ジョブモードを自動判別
CMD ["python", "main.py"]
```

**ポイント:**
- マルチステージビルドでイメージサイズ削減
- `main.py` をエントリポイントに（JOB_TYPE環境変数でサーバー/ジョブ自動切替）
- dev依存を除外（`.[dev]` → `.`）
- `--reload` なし（Hypercorn本番モード）

---

## 4-2. Cloud Run サービス作成

### gcloudコマンド

**Artifact Registryリポジトリ作成（初回のみ）:**
```bash
gcloud artifacts repositories create vimmy-tools \
  --repository-format=docker \
  --location=asia-northeast1 \
  --project=vimmy-459300
```

**Staging:**
```bash
gcloud run deploy stg-vimmy-tools-backend \
  --image=asia-northeast1-docker.pkg.dev/vimmy-459300/vimmy-tools/backend:latest \
  --region=asia-northeast1 \
  --project=vimmy-459300 \
  --platform=managed \
  --memory=512Mi \
  --cpu=1 \
  --min-instances=0 \
  --max-instances=5 \
  --port=8081 \
  --allow-unauthenticated \
  --set-env-vars="ENV=staging" \
  --set-secrets="FIREBASE_PROJECT_ID=FIREBASE_PROJECT_ID:latest,FIREBASE_PRIVATE_KEY=FIREBASE_PRIVATE_KEY:latest,FIREBASE_CLIENT_EMAIL=FIREBASE_CLIENT_EMAIL:latest,FIREBASE_TENANT_ID=FIREBASE_TENANT_ID_STAGING:latest,SLACK_WEBHOOK_URL=SLACK_WEBHOOK_URL:latest,NESSLE_API_KEY=NESSLE_API_KEY:latest,YOUTUBE_API_KEY=YOUTUBE_API_KEY:latest"
```

**Production:**
```bash
gcloud run deploy prd-vimmy-tools-backend \
  --image=asia-northeast1-docker.pkg.dev/vimmy-459300/vimmy-tools/backend:latest \
  --region=asia-northeast1 \
  --project=vimmy-459300 \
  --platform=managed \
  --memory=1Gi \
  --cpu=1 \
  --min-instances=1 \
  --max-instances=10 \
  --port=8081 \
  --allow-unauthenticated \
  --set-env-vars="ENV=production" \
  --set-secrets="FIREBASE_PROJECT_ID=FIREBASE_PROJECT_ID:latest,FIREBASE_PRIVATE_KEY=FIREBASE_PRIVATE_KEY:latest,FIREBASE_CLIENT_EMAIL=FIREBASE_CLIENT_EMAIL:latest,FIREBASE_TENANT_ID=FIREBASE_TENANT_ID_PRODUCTION:latest,SLACK_WEBHOOK_URL=SLACK_WEBHOOK_URL:latest,NESSLE_API_KEY=NESSLE_API_KEY:latest,YOUTUBE_API_KEY=YOUTUBE_API_KEY:latest"
```

### Secret Manager 事前登録（初回のみ）

```bash
# 各シークレットを作成
for secret in FIREBASE_PROJECT_ID FIREBASE_PRIVATE_KEY FIREBASE_CLIENT_EMAIL \
  FIREBASE_TENANT_ID_STAGING FIREBASE_TENANT_ID_PRODUCTION \
  SLACK_WEBHOOK_URL NESSLE_API_KEY YOUTUBE_API_KEY; do
  echo -n "<値>" | gcloud secrets create $secret \
    --data-file=- --project=vimmy-459300
done
```

---

## 4-3. Cloud Run Jobs（28ジョブ）

### ジョブ作成コマンドテンプレート

全ジョブ同一イメージ、`JOB_TYPE` 環境変数で処理を切替。

**Staging用（stg-プレフィックス）:**
```bash
gcloud run jobs create stg-{JOB_NAME} \
  --image=asia-northeast1-docker.pkg.dev/vimmy-459300/vimmy-tools/backend:latest \
  --region=asia-northeast1 \
  --project=vimmy-459300 \
  --task-timeout=3600s \
  --max-retries=1 \
  --set-env-vars="JOB_TYPE={JOB_NAME},ENV=staging" \
  --set-secrets="FIREBASE_PROJECT_ID=FIREBASE_PROJECT_ID:latest,FIREBASE_PRIVATE_KEY=FIREBASE_PRIVATE_KEY:latest,FIREBASE_CLIENT_EMAIL=FIREBASE_CLIENT_EMAIL:latest,FIREBASE_TENANT_ID=FIREBASE_TENANT_ID_STAGING:latest,SLACK_WEBHOOK_URL=SLACK_WEBHOOK_URL:latest,NESSLE_API_KEY=NESSLE_API_KEY:latest,YOUTUBE_API_KEY=YOUTUBE_API_KEY:latest" \
  --memory=1Gi \
  --cpu=1
```

**Production用（prd-プレフィックス）:**
```bash
gcloud run jobs create prd-{JOB_NAME} \
  --image=asia-northeast1-docker.pkg.dev/vimmy-459300/vimmy-tools/backend:latest \
  --region=asia-northeast1 \
  --project=vimmy-459300 \
  --task-timeout=3600s \
  --max-retries=1 \
  --set-env-vars="JOB_TYPE={JOB_NAME},ENV=production" \
  --set-secrets="FIREBASE_PROJECT_ID=FIREBASE_PROJECT_ID:latest,FIREBASE_PRIVATE_KEY=FIREBASE_PRIVATE_KEY:latest,FIREBASE_CLIENT_EMAIL=FIREBASE_CLIENT_EMAIL:latest,FIREBASE_TENANT_ID=FIREBASE_TENANT_ID_PRODUCTION:latest,SLACK_WEBHOOK_URL=SLACK_WEBHOOK_URL:latest,NESSLE_API_KEY=NESSLE_API_KEY:latest,YOUTUBE_API_KEY=YOUTUBE_API_KEY:latest" \
  --memory=2Gi \
  --cpu=1
```

### 全28ジョブ一覧（{JOB_NAME}に代入）

| # | JOB_NAME | カテゴリ |
|---|---|---|
| 1 | tools-instagram-metric-collector | Instagram |
| 2 | tools-instagram-account-daily-updater | Instagram |
| 3 | tools-youtube-metrics-collector | YouTube |
| 4 | tools-youtube-account-daily-updater | YouTube |
| 5 | tools-qoo10-shop-scraper | Qoo10 |
| 6 | tools-qoo10-brand-scraper | Qoo10 |
| 7 | tools-qoo10-ranking-scraper | Qoo10 |
| 8 | tools-lemon8-influencer-scraper | Lemon8 |
| 9 | tools-lemon8-metrics-collector | Lemon8 |
| 10 | tools-lemon8-account-daily-updater | Lemon8 |
| 11 | tools-buzz-tools-job | Buzz Tools |
| 12 | tools-prtimes-scraper | 営業リード |
| 13 | tools-gbizinfo-scraper | 営業リード |
| 14 | tools-rakuten-scraper | 営業リード |
| 15 | tools-yahoo-shopping-scraper | 営業リード |
| 16 | tools-amazon-scraper | 営業リード |
| 17 | tools-google-maps-scraper | 営業リード |
| 18 | tools-youtube-leads-scraper | 営業リード |
| 19 | tools-makuake-scraper | 営業リード |
| 20 | tools-hotpepper-scraper | 営業リード |
| 21 | tools-base-ec-scraper | 営業リード |
| 22 | tools-campfire-scraper | 営業リード |
| 23 | tools-migrate-to-sales-leads | 営業リード |
| 24 | tools-cosme-scraper | 営業リード |
| 25 | tools-itownpage-scraper | 営業リード |
| 26 | tools-minne-scraper | 営業リード |
| 27 | tools-tabelog-scraper | 営業リード |
| 28 | tools-wantedly-scraper | 営業リード |

### ジョブ一括作成スクリプト

**作成ファイル:** `scripts/create-cloud-run-jobs.sh`

```bash
#!/bin/bash
set -e

ENV_PREFIX=$1  # "stg" or "prd"
ENV_NAME=$2    # "staging" or "production"
TENANT_SECRET=$3  # "FIREBASE_TENANT_ID_STAGING" or "FIREBASE_TENANT_ID_PRODUCTION"
MEMORY=${4:-"1Gi"}

JOBS=(
  tools-instagram-metric-collector
  tools-instagram-account-daily-updater
  tools-youtube-metrics-collector
  tools-youtube-account-daily-updater
  tools-qoo10-shop-scraper
  tools-qoo10-brand-scraper
  tools-qoo10-ranking-scraper
  tools-lemon8-influencer-scraper
  tools-lemon8-metrics-collector
  tools-lemon8-account-daily-updater
  tools-buzz-tools-job
  tools-prtimes-scraper
  tools-gbizinfo-scraper
  tools-rakuten-scraper
  tools-yahoo-shopping-scraper
  tools-amazon-scraper
  tools-google-maps-scraper
  tools-youtube-leads-scraper
  tools-makuake-scraper
  tools-hotpepper-scraper
  tools-base-ec-scraper
  tools-campfire-scraper
  tools-migrate-to-sales-leads
  tools-cosme-scraper
  tools-itownpage-scraper
  tools-minne-scraper
  tools-tabelog-scraper
  tools-wantedly-scraper
)

for job in "${JOBS[@]}"; do
  echo "Creating ${ENV_PREFIX}-${job}..."
  gcloud run jobs create "${ENV_PREFIX}-${job}" \
    --image=asia-northeast1-docker.pkg.dev/vimmy-459300/vimmy-tools/backend:latest \
    --region=asia-northeast1 \
    --project=vimmy-459300 \
    --task-timeout=3600s \
    --max-retries=1 \
    --set-env-vars="JOB_TYPE=${job},ENV=${ENV_NAME}" \
    --set-secrets="FIREBASE_PROJECT_ID=FIREBASE_PROJECT_ID:latest,FIREBASE_PRIVATE_KEY=FIREBASE_PRIVATE_KEY:latest,FIREBASE_CLIENT_EMAIL=FIREBASE_CLIENT_EMAIL:latest,FIREBASE_TENANT_ID=${TENANT_SECRET}:latest,SLACK_WEBHOOK_URL=SLACK_WEBHOOK_URL:latest,NESSLE_API_KEY=NESSLE_API_KEY:latest,YOUTUBE_API_KEY=YOUTUBE_API_KEY:latest" \
    --memory="${MEMORY}" \
    --cpu=1
  echo "✓ ${ENV_PREFIX}-${job} created"
done
```

**実行:**
```bash
# Staging
bash scripts/create-cloud-run-jobs.sh stg staging FIREBASE_TENANT_ID_STAGING 1Gi

# Production
bash scripts/create-cloud-run-jobs.sh prd production FIREBASE_TENANT_ID_PRODUCTION 2Gi
```

---

## 4-4. Cloud Scheduler

### スケジュール定義

Cloud Schedulerで各ジョブの定期実行を設定。Production環境のみ（Stagingは手動実行）。

**gcloudコマンドテンプレート:**
```bash
gcloud scheduler jobs create http prd-{JOB_NAME}-schedule \
  --location=asia-northeast1 \
  --project=vimmy-459300 \
  --schedule="{CRON}" \
  --time-zone="Asia/Tokyo" \
  --uri="https://asia-northeast1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/vimmy-459300/jobs/prd-{JOB_NAME}:run" \
  --http-method=POST \
  --oauth-service-account-email=terraform-prod-sa@vimmy-459300.iam.gserviceaccount.com
```

### 推奨スケジュール一覧

| # | ジョブ名 | cron式 | 説明 |
|---|---|---|---|
| **Instagram** | | | |
| 1 | tools-instagram-metric-collector | `0 3 * * *` | 毎日3:00 メトリクス収集 |
| 2 | tools-instagram-account-daily-updater | `0 5 * * *` | 毎日5:00 アカウント更新 |
| **YouTube** | | | |
| 3 | tools-youtube-metrics-collector | `0 4 * * *` | 毎日4:00 メトリクス収集 |
| 4 | tools-youtube-account-daily-updater | `0 6 * * *` | 毎日6:00 アカウント更新 |
| **Qoo10** | | | |
| 5 | tools-qoo10-shop-scraper | `0 2 * * 1` | 毎週月曜2:00 |
| 6 | tools-qoo10-brand-scraper | `0 2 * * 3` | 毎週水曜2:00 |
| 7 | tools-qoo10-ranking-scraper | `0 1 * * *` | 毎日1:00 |
| **Lemon8** | | | |
| 8 | tools-lemon8-influencer-scraper | `0 2 * * 2` | 毎週火曜2:00 |
| 9 | tools-lemon8-metrics-collector | `0 3 * * *` | 毎日3:00（※Instagram後） |
| 10 | tools-lemon8-account-daily-updater | `0 5 * * *` | 毎日5:00 |
| **Buzz Tools** | | | |
| 11 | tools-buzz-tools-job | `0 7 * * *` | 毎日7:00 |
| **営業リード** | | | |
| 12 | tools-prtimes-scraper | `0 8 * * 1` | 毎週月曜8:00 |
| 13 | tools-gbizinfo-scraper | `0 8 * * 2` | 毎週火曜8:00 |
| 14 | tools-rakuten-scraper | `0 9 * * 1` | 毎週月曜9:00 |
| 15 | tools-yahoo-shopping-scraper | `0 9 * * 2` | 毎週火曜9:00 |
| 16 | tools-amazon-scraper | `0 10 * * 1` | 毎週月曜10:00 |
| 17 | tools-google-maps-scraper | `0 10 * * 2` | 毎週火曜10:00 |
| 18 | tools-youtube-leads-scraper | `0 11 * * 1` | 毎週月曜11:00 |
| 19 | tools-makuake-scraper | `0 11 * * 2` | 毎週火曜11:00 |
| 20 | tools-hotpepper-scraper | `0 8 * * 3` | 毎週水曜8:00 |
| 21 | tools-base-ec-scraper | `0 9 * * 3` | 毎週水曜9:00 |
| 22 | tools-campfire-scraper | `0 10 * * 3` | 毎週水曜10:00 |
| 23 | tools-cosme-scraper | `0 8 * * 4` | 毎週木曜8:00 |
| 24 | tools-itownpage-scraper | `0 9 * * 4` | 毎週木曜9:00 |
| 25 | tools-minne-scraper | `0 10 * * 4` | 毎週木曜10:00 |
| 26 | tools-tabelog-scraper | `0 8 * * 5` | 毎週金曜8:00 |
| 27 | tools-wantedly-scraper | `0 9 * * 5` | 毎週金曜9:00 |
| 28 | tools-migrate-to-sales-leads | `0 0 1 * *` | 毎月1日0:00（移行用） |

> **注意:** 上記のcron式は推奨値。Vimmyの既存スケジュールに合わせて調整する必要がある。

### スケジューラー一括作成スクリプト

**作成ファイル:** `scripts/create-cloud-scheduler.sh`

```bash
#!/bin/bash
set -e

SA_EMAIL="terraform-prod-sa@vimmy-459300.iam.gserviceaccount.com"

create_schedule() {
  local job_name=$1
  local cron=$2
  local description=$3

  echo "Creating schedule for prd-${job_name}..."
  gcloud scheduler jobs create http "prd-${job_name}-schedule" \
    --location=asia-northeast1 \
    --project=vimmy-459300 \
    --schedule="${cron}" \
    --time-zone="Asia/Tokyo" \
    --uri="https://asia-northeast1-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/vimmy-459300/jobs/prd-${job_name}:run" \
    --http-method=POST \
    --oauth-service-account-email="${SA_EMAIL}" \
    --description="${description}"
  echo "✓ prd-${job_name}-schedule created"
}

# Instagram
create_schedule "tools-instagram-metric-collector"      "0 3 * * *"   "Instagram メトリクス収集"
create_schedule "tools-instagram-account-daily-updater"  "0 5 * * *"   "Instagram アカウント日次更新"

# YouTube
create_schedule "tools-youtube-metrics-collector"        "0 4 * * *"   "YouTube メトリクス収集"
create_schedule "tools-youtube-account-daily-updater"    "0 6 * * *"   "YouTube アカウント日次更新"

# Qoo10
create_schedule "tools-qoo10-shop-scraper"              "0 2 * * 1"   "Qoo10 ショップスクレイピング（週次）"
create_schedule "tools-qoo10-brand-scraper"             "0 2 * * 3"   "Qoo10 ブランドスクレイピング（週次）"
create_schedule "tools-qoo10-ranking-scraper"           "0 1 * * *"   "Qoo10 ランキングスクレイピング（日次）"

# Lemon8
create_schedule "tools-lemon8-influencer-scraper"       "0 2 * * 2"   "Lemon8 インフルエンサースクレイピング（週次）"
create_schedule "tools-lemon8-metrics-collector"        "0 3 * * *"   "Lemon8 メトリクス収集"
create_schedule "tools-lemon8-account-daily-updater"    "0 5 * * *"   "Lemon8 アカウント日次更新"

# Buzz Tools
create_schedule "tools-buzz-tools-job"                  "0 7 * * *"   "バズツール実行"

# 営業リード（月〜金に分散）
create_schedule "tools-prtimes-scraper"                 "0 8 * * 1"   "PR TIMES スクレイピング"
create_schedule "tools-gbizinfo-scraper"                "0 8 * * 2"   "gBizINFO スクレイピング"
create_schedule "tools-rakuten-scraper"                 "0 9 * * 1"   "楽天 スクレイピング"
create_schedule "tools-yahoo-shopping-scraper"          "0 9 * * 2"   "Yahoo!ショッピング スクレイピング"
create_schedule "tools-amazon-scraper"                  "0 10 * * 1"  "Amazon スクレイピング"
create_schedule "tools-google-maps-scraper"             "0 10 * * 2"  "Google Maps スクレイピング"
create_schedule "tools-youtube-leads-scraper"           "0 11 * * 1"  "YouTube Leads スクレイピング"
create_schedule "tools-makuake-scraper"                 "0 11 * * 2"  "Makuake スクレイピング"
create_schedule "tools-hotpepper-scraper"               "0 8 * * 3"   "ホットペッパー スクレイピング"
create_schedule "tools-base-ec-scraper"                 "0 9 * * 3"   "Base EC スクレイピング"
create_schedule "tools-campfire-scraper"                "0 10 * * 3"  "Campfire スクレイピング"
create_schedule "tools-cosme-scraper"                   "0 8 * * 4"   "@cosme スクレイピング"
create_schedule "tools-itownpage-scraper"               "0 9 * * 4"   "iタウンページ スクレイピング"
create_schedule "tools-minne-scraper"                   "0 10 * * 4"  "minne スクレイピング"
create_schedule "tools-tabelog-scraper"                 "0 8 * * 5"   "食べログ スクレイピング"
create_schedule "tools-wantedly-scraper"                "0 9 * * 5"   "Wantedly スクレイピング"
create_schedule "tools-migrate-to-sales-leads"          "0 0 1 * *"   "営業リード移行（月次）"

echo "All schedules created successfully!"
```

---

## 4-5. Firebase Hosting

### サイト作成

```bash
firebase hosting:sites:create vimmy-tools-dashboard --project=vimmy-459300
firebase hosting:sites:create vimmy-tools-dashboard-staging --project=vimmy-459300
```

### 作成ファイル: `frontend/firebase.json`

```json
{
  "hosting": [
    {
      "site": "vimmy-tools-dashboard",
      "public": "tools-dashboard/dist",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
      "rewrites": [
        {
          "source": "**",
          "destination": "/index.html"
        }
      ],
      "headers": [
        {
          "source": "/assets/**",
          "headers": [
            {
              "key": "Cache-Control",
              "value": "public, max-age=31536000, immutable"
            }
          ]
        }
      ]
    },
    {
      "site": "vimmy-tools-dashboard-staging",
      "public": "tools-dashboard/dist",
      "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
      "rewrites": [
        {
          "source": "**",
          "destination": "/index.html"
        }
      ]
    }
  ]
}
```

### 作成ファイル: `frontend/.firebaserc`

```json
{
  "projects": {
    "default": "vimmy-459300"
  },
  "targets": {
    "vimmy-459300": {
      "hosting": {
        "production": ["vimmy-tools-dashboard"],
        "staging": ["vimmy-tools-dashboard-staging"]
      }
    }
  }
}
```

---

## 4-6. GitHub Actions（4ワークフロー）

### ワークフロー1: `.github/workflows/deploy-stg-backend.yml`

```yaml
name: Deploy Staging Backend

on:
  push:
    branches:
      - 'release'
      - 'release_*'
    paths:
      - 'backend/**'
      - '.github/workflows/deploy-stg-backend.yml'

env:
  PROJECT_ID: vimmy-459300
  REGION: asia-northeast1
  SERVICE_NAME: stg-vimmy-tools-backend
  REPOSITORY: vimmy-tools
  IMAGE_NAME: backend

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Configure Docker
        run: gcloud auth configure-docker asia-northeast1-docker.pkg.dev

      - name: Build Docker image
        run: |
          docker build \
            -f backend/Dockerfile.prod \
            -t asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -t asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:latest \
            backend/

      - name: Push Docker image
        run: |
          docker push asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          docker push asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:latest

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy ${{ env.SERVICE_NAME }} \
            --image=asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --region=${{ env.REGION }} \
            --project=${{ env.PROJECT_ID }}

      - name: Update Cloud Run Jobs (Staging)
        run: |
          JOBS=(
            stg-tools-instagram-metric-collector
            stg-tools-instagram-account-daily-updater
            stg-tools-youtube-metrics-collector
            stg-tools-youtube-account-daily-updater
            stg-tools-qoo10-shop-scraper
            stg-tools-qoo10-brand-scraper
            stg-tools-qoo10-ranking-scraper
            stg-tools-lemon8-influencer-scraper
            stg-tools-lemon8-metrics-collector
            stg-tools-lemon8-account-daily-updater
            stg-tools-buzz-tools-job
            stg-tools-prtimes-scraper
            stg-tools-gbizinfo-scraper
            stg-tools-rakuten-scraper
            stg-tools-yahoo-shopping-scraper
            stg-tools-amazon-scraper
            stg-tools-google-maps-scraper
            stg-tools-youtube-leads-scraper
            stg-tools-makuake-scraper
            stg-tools-hotpepper-scraper
            stg-tools-base-ec-scraper
            stg-tools-campfire-scraper
            stg-tools-migrate-to-sales-leads
            stg-tools-cosme-scraper
            stg-tools-itownpage-scraper
            stg-tools-minne-scraper
            stg-tools-tabelog-scraper
            stg-tools-wantedly-scraper
          )
          for job in "${JOBS[@]}"; do
            echo "Updating ${job}..."
            gcloud run jobs update "${job}" \
              --image=asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
              --region=${{ env.REGION }} \
              --project=${{ env.PROJECT_ID }} || echo "Warning: Failed to update ${job}"
          done
```

### ワークフロー2: `.github/workflows/deploy-prd-backend.yml`

```yaml
name: Deploy Production Backend

on:
  push:
    branches:
      - 'main'
    paths:
      - 'backend/**'
      - '.github/workflows/deploy-prd-backend.yml'

env:
  PROJECT_ID: vimmy-459300
  REGION: asia-northeast1
  SERVICE_NAME: prd-vimmy-tools-backend
  REPOSITORY: vimmy-tools
  IMAGE_NAME: backend

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Set up Cloud SDK
        uses: google-github-actions/setup-gcloud@v2

      - name: Configure Docker
        run: gcloud auth configure-docker asia-northeast1-docker.pkg.dev

      - name: Build Docker image
        run: |
          docker build \
            -f backend/Dockerfile.prod \
            -t asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            -t asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:latest-prod \
            backend/

      - name: Push Docker image
        run: |
          docker push asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          docker push asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:latest-prod

      - name: Deploy to Cloud Run
        run: |
          gcloud run deploy ${{ env.SERVICE_NAME }} \
            --image=asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
            --region=${{ env.REGION }} \
            --project=${{ env.PROJECT_ID }}

      - name: Update Cloud Run Jobs (Production)
        run: |
          JOBS=(
            prd-tools-instagram-metric-collector
            prd-tools-instagram-account-daily-updater
            prd-tools-youtube-metrics-collector
            prd-tools-youtube-account-daily-updater
            prd-tools-qoo10-shop-scraper
            prd-tools-qoo10-brand-scraper
            prd-tools-qoo10-ranking-scraper
            prd-tools-lemon8-influencer-scraper
            prd-tools-lemon8-metrics-collector
            prd-tools-lemon8-account-daily-updater
            prd-tools-buzz-tools-job
            prd-tools-prtimes-scraper
            prd-tools-gbizinfo-scraper
            prd-tools-rakuten-scraper
            prd-tools-yahoo-shopping-scraper
            prd-tools-amazon-scraper
            prd-tools-google-maps-scraper
            prd-tools-youtube-leads-scraper
            prd-tools-makuake-scraper
            prd-tools-hotpepper-scraper
            prd-tools-base-ec-scraper
            prd-tools-campfire-scraper
            prd-tools-migrate-to-sales-leads
            prd-tools-cosme-scraper
            prd-tools-itownpage-scraper
            prd-tools-minne-scraper
            prd-tools-tabelog-scraper
            prd-tools-wantedly-scraper
          )
          for job in "${JOBS[@]}"; do
            echo "Updating ${job}..."
            gcloud run jobs update "${job}" \
              --image=asia-northeast1-docker.pkg.dev/${{ env.PROJECT_ID }}/${{ env.REPOSITORY }}/${{ env.IMAGE_NAME }}:${{ github.sha }} \
              --region=${{ env.REGION }} \
              --project=${{ env.PROJECT_ID }} || echo "Warning: Failed to update ${job}"
          done
```

### ワークフロー3: `.github/workflows/deploy-stg-frontend.yml`

```yaml
name: Deploy Staging Frontend

on:
  push:
    branches:
      - 'release'
      - 'release_*'
    paths:
      - 'frontend/**'
      - '.github/workflows/deploy-stg-frontend.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Install dependencies
        working-directory: frontend
        run: pnpm install --frozen-lockfile

      - name: Build
        working-directory: frontend
        run: pnpm build
        env:
          VITE_ENV: staging
          VITE_API_URL: ${{ secrets.STG_API_URL }}
          VITE_FIREBASE_API_KEY: ${{ secrets.FIREBASE_API_KEY }}
          VITE_FIREBASE_AUTH_DOMAIN: ${{ secrets.FIREBASE_AUTH_DOMAIN }}
          VITE_FIREBASE_PROJECT_ID: ${{ secrets.FIREBASE_PROJECT_ID }}
          VITE_FIREBASE_STORAGE_BUCKET: ${{ secrets.FIREBASE_STORAGE_BUCKET }}
          VITE_FIREBASE_MESSAGE_SENDER_ID: ${{ secrets.FIREBASE_MESSAGE_SENDER_ID }}
          VITE_FIREBASE_APP_ID: ${{ secrets.FIREBASE_APP_ID }}
          VITE_FIREBASE_TENANT_ID: ${{ secrets.STG_FIREBASE_TENANT_ID }}

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Install Firebase CLI
        run: npm install -g firebase-tools

      - name: Deploy to Firebase Hosting (Staging)
        working-directory: frontend
        run: firebase deploy --only hosting:staging --project=vimmy-459300
```

### ワークフロー4: `.github/workflows/deploy-prd-frontend.yml`

```yaml
name: Deploy Production Frontend

on:
  push:
    branches:
      - 'main'
    paths:
      - 'frontend/**'
      - '.github/workflows/deploy-prd-frontend.yml'

jobs:
  deploy:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '22'

      - name: Setup pnpm
        uses: pnpm/action-setup@v4
        with:
          version: 9

      - name: Install dependencies
        working-directory: frontend
        run: pnpm install --frozen-lockfile

      - name: Build
        working-directory: frontend
        run: pnpm build
        env:
          VITE_ENV: production
          VITE_API_URL: ${{ secrets.PRD_API_URL }}
          VITE_FIREBASE_API_KEY: ${{ secrets.FIREBASE_API_KEY }}
          VITE_FIREBASE_AUTH_DOMAIN: ${{ secrets.FIREBASE_AUTH_DOMAIN }}
          VITE_FIREBASE_PROJECT_ID: ${{ secrets.FIREBASE_PROJECT_ID }}
          VITE_FIREBASE_STORAGE_BUCKET: ${{ secrets.FIREBASE_STORAGE_BUCKET }}
          VITE_FIREBASE_MESSAGE_SENDER_ID: ${{ secrets.FIREBASE_MESSAGE_SENDER_ID }}
          VITE_FIREBASE_APP_ID: ${{ secrets.FIREBASE_APP_ID }}
          VITE_FIREBASE_TENANT_ID: ${{ secrets.PRD_FIREBASE_TENANT_ID }}

      - name: Authenticate to Google Cloud
        uses: google-github-actions/auth@v2
        with:
          workload_identity_provider: ${{ secrets.WIF_PROVIDER }}
          service_account: ${{ secrets.WIF_SERVICE_ACCOUNT }}

      - name: Install Firebase CLI
        run: npm install -g firebase-tools

      - name: Deploy to Firebase Hosting (Production)
        working-directory: frontend
        run: firebase deploy --only hosting:production --project=vimmy-459300
```

---

## 4-7. GitHub Secrets 設定

GitHub Actions で必要なSecrets一覧:

| Secret名 | 用途 |
|---|---|
| `WIF_PROVIDER` | Workload Identity Federation プロバイダ |
| `WIF_SERVICE_ACCOUNT` | サービスアカウントメール |
| `STG_API_URL` | ステージングAPI URL（例: `https://stg-vimmy-tools-backend-xxxxx.run.app`） |
| `PRD_API_URL` | 本番API URL（例: `https://prd-vimmy-tools-backend-xxxxx.run.app`） |
| `FIREBASE_API_KEY` | Firebase公開APIキー |
| `FIREBASE_AUTH_DOMAIN` | `vimmy-459300.firebaseapp.com` |
| `FIREBASE_PROJECT_ID` | `vimmy-459300` |
| `FIREBASE_STORAGE_BUCKET` | `vimmy-459300.firebasestorage.app` |
| `FIREBASE_MESSAGE_SENDER_ID` | FCM送信者ID |
| `FIREBASE_APP_ID` | Firebaseアプリ ID |
| `STG_FIREBASE_TENANT_ID` | ステージング用テナントID |
| `PRD_FIREBASE_TENANT_ID` | 本番用テナントID |

---

## 作成・変更ファイル一覧

| # | ファイルパス | 種別 |
|---|---|---|
| 1 | `backend/Dockerfile.prod` | 新規作成 |
| 2 | `frontend/firebase.json` | 新規作成 |
| 3 | `frontend/.firebaserc` | 新規作成 |
| 4 | `.github/workflows/deploy-stg-backend.yml` | 新規作成 |
| 5 | `.github/workflows/deploy-prd-backend.yml` | 新規作成 |
| 6 | `.github/workflows/deploy-stg-frontend.yml` | 新規作成 |
| 7 | `.github/workflows/deploy-prd-frontend.yml` | 新規作成 |
| 8 | `scripts/create-cloud-run-jobs.sh` | 新規作成 |
| 9 | `scripts/create-cloud-scheduler.sh` | 新規作成 |

---

## 実行順序

### Step 1: GCPリソース準備（手動/CLI）
1. Secret Managerにシークレット登録
2. Artifact Registryリポジトリ作成
3. Workload Identity Federation設定（GitHub Actions ↔ GCP連携）

### Step 2: ファイル作成
1. `backend/Dockerfile.prod` 作成
2. `frontend/firebase.json` + `.firebaserc` 作成
3. 4つのGitHub Actionsワークフロー作成
4. `scripts/create-cloud-run-jobs.sh` 作成
5. `scripts/create-cloud-scheduler.sh` 作成

### Step 3: Firebase Hosting初期設定
```bash
firebase hosting:sites:create vimmy-tools-dashboard --project=vimmy-459300
firebase hosting:sites:create vimmy-tools-dashboard-staging --project=vimmy-459300
```

### Step 4: Cloud Runサービス初回デプロイ
```bash
# イメージビルド＆プッシュ
docker build -f backend/Dockerfile.prod -t asia-northeast1-docker.pkg.dev/vimmy-459300/vimmy-tools/backend:initial backend/
docker push asia-northeast1-docker.pkg.dev/vimmy-459300/vimmy-tools/backend:initial

# Stagingサービス作成
gcloud run deploy stg-vimmy-tools-backend ...

# Productionサービス作成
gcloud run deploy prd-vimmy-tools-backend ...
```

### Step 5: Cloud Run Jobs作成
```bash
bash scripts/create-cloud-run-jobs.sh stg staging FIREBASE_TENANT_ID_STAGING 1Gi
bash scripts/create-cloud-run-jobs.sh prd production FIREBASE_TENANT_ID_PRODUCTION 2Gi
```

### Step 6: Cloud Scheduler設定
```bash
bash scripts/create-cloud-scheduler.sh
```

### Step 7: GitHub Secrets設定
GitHub UIまたは `gh secret set` で全Secretsを登録

### Step 8: CI/CDテスト
releaseブランチへpush → Stagingデプロイ確認

---

## 検証チェックリスト

### Cloud Run サービス
- [ ] ステージングAPI: `https://stg-vimmy-tools-backend-xxxxx.run.app/docs` でOpenAPIドキュメント表示
- [ ] 本番API: `https://prd-vimmy-tools-backend-xxxxx.run.app/docs` でOpenAPIドキュメント表示
- [ ] CORS設定: フロントエンドからのAPI呼び出し成功
- [ ] 認証: Firebase IDトークン付きリクエストが認証される

### Cloud Run Jobs
- [ ] ステージングジョブ1つを手動実行 → 正常完了
- [ ] Slack通知が届く
- [ ] `make run-job-staging` からジョブ起動可能

### Firebase Hosting
- [ ] `https://vimmy-tools-dashboard-staging.web.app` アクセス可能
- [ ] `https://vimmy-tools-dashboard.web.app` アクセス可能
- [ ] SPAルーティング（直接URL入力でも正しくレンダリング）

### CI/CD パイプライン
- [ ] releaseブランチpush → Staging バックエンドデプロイ成功
- [ ] releaseブランチpush → Staging フロントエンドデプロイ成功
- [ ] mainブランチpush → Production バックエンドデプロイ成功
- [ ] mainブランチpush → Production フロントエンドデプロイ成功
- [ ] バックエンドデプロイ時にCloud Run Jobsのイメージも更新される

### Cloud Scheduler
- [ ] スケジューラー設定確認: `gcloud scheduler jobs list --project=vimmy-459300 --location=asia-northeast1`
- [ ] テスト実行: `gcloud scheduler jobs run prd-tools-qoo10-ranking-scraper-schedule --project=vimmy-459300 --location=asia-northeast1`
