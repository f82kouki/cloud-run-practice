.PHONY: dev down build build-prod logs shell-backend shell-frontend health job

# ローカル開発
dev:
	docker compose up

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f

# 本番用イメージのビルド確認
build-prod:
	docker build -f backend/Dockerfile.prod -t practice-backend backend/

# コンテナ内シェル
shell-backend:
	docker compose exec backend bash

shell-frontend:
	docker compose exec frontend sh

# ヘルスチェック
health:
	curl -s http://localhost:8081/health | python3 -m json.tool

# Cloud Run Jobs 動作確認
# 例: make job JOB_TYPE=tools-instagram-metric-collector
job: build-prod
	docker run --rm -e JOB_TYPE=$(JOB_TYPE) practice-backend
