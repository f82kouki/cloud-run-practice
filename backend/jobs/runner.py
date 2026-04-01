import sys


JOB_HANDLERS: dict[str, str] = {
    "scout-email-sender": "スカウトメール一括送信",
    "student-data-sync": "学生データ同期",
    "matching-score-calculator": "マッチングスコア計算",
    "weekly-report-generator": "週次レポート生成",
    "inactive-student-cleanup": "非アクティブ学生整理",
    "scout-reminder-sender": "スカウトリマインド送信",
}


def run_job(job_type: str) -> None:
    description = JOB_HANDLERS.get(job_type)
    if description is None:
        print(f"[ERROR] Unknown JOB_TYPE: {job_type}", file=sys.stderr)
        sys.exit(1)

    print(f"[JOB] Starting: {job_type} ({description})")
    # ここに実際のジョブ処理を実装する
    print(f"[JOB] Done: {job_type}")
