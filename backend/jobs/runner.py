import sys


JOB_HANDLERS: dict[str, str] = {
    "tools-instagram-metric-collector": "Instagram メトリクス収集",
    "tools-instagram-account-daily-updater": "Instagram アカウント日次更新",
    "tools-youtube-metrics-collector": "YouTube メトリクス収集",
    "tools-youtube-account-daily-updater": "YouTube アカウント日次更新",
    "tools-qoo10-shop-scraper": "Qoo10 ショップスクレイピング",
    "tools-qoo10-brand-scraper": "Qoo10 ブランドスクレイピング",
    "tools-qoo10-ranking-scraper": "Qoo10 ランキングスクレイピング",
    "tools-lemon8-influencer-scraper": "Lemon8 インフルエンサースクレイピング",
    "tools-lemon8-metrics-collector": "Lemon8 メトリクス収集",
    "tools-lemon8-account-daily-updater": "Lemon8 アカウント日次更新",
    "tools-buzz-tools-job": "バズツール実行",
    "tools-prtimes-scraper": "PR TIMES スクレイピング",
    "tools-gbizinfo-scraper": "gBizINFO スクレイピング",
    "tools-rakuten-scraper": "楽天スクレイピング",
    "tools-yahoo-shopping-scraper": "Yahoo!ショッピングスクレイピング",
    "tools-amazon-scraper": "Amazon スクレイピング",
    "tools-google-maps-scraper": "Google Maps スクレイピング",
    "tools-youtube-leads-scraper": "YouTube Leads スクレイピング",
    "tools-makuake-scraper": "Makuake スクレイピング",
    "tools-hotpepper-scraper": "ホットペッパースクレイピング",
    "tools-base-ec-scraper": "Base EC スクレイピング",
    "tools-campfire-scraper": "Campfire スクレイピング",
    "tools-migrate-to-sales-leads": "営業リード移行",
    "tools-cosme-scraper": "@cosme スクレイピング",
    "tools-itownpage-scraper": "iタウンページスクレイピング",
    "tools-minne-scraper": "minne スクレイピング",
    "tools-tabelog-scraper": "食べログスクレイピング",
    "tools-wantedly-scraper": "Wantedly スクレイピング",
}


def run_job(job_type: str) -> None:
    description = JOB_HANDLERS.get(job_type)
    if description is None:
        print(f"[ERROR] Unknown JOB_TYPE: {job_type}", file=sys.stderr)
        sys.exit(1)

    print(f"[JOB] Starting: {job_type} ({description})")
    # ここに実際のジョブ処理を実装する
    print(f"[JOB] Done: {job_type}")
