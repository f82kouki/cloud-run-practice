#!/bin/bash
set -e

# 使い方: bash scripts/create-cloud-run-jobs.sh <stg|prd> <staging|production>
# 例: bash scripts/create-cloud-run-jobs.sh stg staging

ENV_PREFIX=$1  # "stg" or "prd"
ENV_NAME=$2    # "staging" or "production"
PROJECT_ID="aston-486600"
REGION="asia-northeast1"
IMAGE="asia-northeast1-docker.pkg.dev/${PROJECT_ID}/scout-platform/backend:latest"

if [ -z "$ENV_PREFIX" ] || [ -z "$ENV_NAME" ]; then
  echo "Usage: bash $0 <stg|prd> <staging|production>"
  exit 1
fi

JOBS=(
  scout-email-sender
  student-data-sync
  matching-score-calculator
  weekly-report-generator
  inactive-student-cleanup
  scout-reminder-sender
)

for job in "${JOBS[@]}"; do
  JOB_NAME="${ENV_PREFIX}-${job}"
  echo "Creating ${JOB_NAME}..."
  gcloud run jobs create "${JOB_NAME}" \
    --image="${IMAGE}" \
    --region="${REGION}" \
    --project="${PROJECT_ID}" \
    --task-timeout=3600s \
    --max-retries=1 \
    --set-env-vars="JOB_TYPE=${job},ENV=${ENV_NAME}" \
    --memory=512Mi \
    --cpu=1
  echo "Done: ${JOB_NAME}"
done

echo "All ${ENV_PREFIX} jobs created!"
