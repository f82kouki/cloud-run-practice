#!/bin/bash
set -e

# Production 環境のジョブを定期実行するスケジューラーを作成
# 使い方: bash scripts/create-cloud-scheduler.sh

PROJECT_ID="aston-486600"
REGION="asia-northeast1"
SA_EMAIL="github-actions-sa@${PROJECT_ID}.iam.gserviceaccount.com"

create_schedule() {
  local job_name=$1
  local cron=$2
  local description=$3

  echo "Creating schedule for prd-${job_name}..."
  gcloud scheduler jobs create http "prd-${job_name}-schedule" \
    --location="${REGION}" \
    --project="${PROJECT_ID}" \
    --schedule="${cron}" \
    --time-zone="Asia/Tokyo" \
    --uri="https://${REGION}-run.googleapis.com/apis/run.googleapis.com/v1/namespaces/${PROJECT_ID}/jobs/prd-${job_name}:run" \
    --http-method=POST \
    --oauth-service-account-email="${SA_EMAIL}" \
    --description="${description}"
  echo "Done: prd-${job_name}-schedule"
}

# スカウトメール送信: 毎日 9:00
create_schedule "scout-email-sender" "0 9 * * *" "スカウトメール一括送信"

# 学生データ同期: 毎日 3:00
create_schedule "student-data-sync" "0 3 * * *" "学生データ同期"

# マッチングスコア計算: 毎日 4:00
create_schedule "matching-score-calculator" "0 4 * * *" "マッチングスコア計算"

# 週次レポート生成: 毎週月曜 8:00
create_schedule "weekly-report-generator" "0 8 * * 1" "週次レポート生成"

# 非アクティブ学生整理: 毎月1日 2:00
create_schedule "inactive-student-cleanup" "0 2 1 * *" "非アクティブ学生整理"

# スカウトリマインド送信: 毎日 10:00
create_schedule "scout-reminder-sender" "0 10 * * *" "スカウトリマインド送信"

echo "All schedules created!"
