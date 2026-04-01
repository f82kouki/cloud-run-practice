from fastapi import APIRouter
from app.models import JobStatus

router = APIRouter()

MOCK_JOBS = [
    # Instagram
    JobStatus(job_name="tools-instagram-metric-collector", category="Instagram", status="success", last_run="2026-04-01T03:00:00+09:00", next_run="2026-04-02T03:00:00+09:00"),
    JobStatus(job_name="tools-instagram-account-daily-updater", category="Instagram", status="success", last_run="2026-04-01T05:00:00+09:00", next_run="2026-04-02T05:00:00+09:00"),
    # YouTube
    JobStatus(job_name="tools-youtube-metrics-collector", category="YouTube", status="success", last_run="2026-04-01T04:00:00+09:00", next_run="2026-04-02T04:00:00+09:00"),
    JobStatus(job_name="tools-youtube-account-daily-updater", category="YouTube", status="failed", last_run="2026-04-01T06:00:00+09:00", next_run="2026-04-02T06:00:00+09:00"),
    # Qoo10
    JobStatus(job_name="tools-qoo10-shop-scraper", category="Qoo10", status="idle", last_run="2026-03-31T02:00:00+09:00", next_run="2026-04-07T02:00:00+09:00"),
    JobStatus(job_name="tools-qoo10-brand-scraper", category="Qoo10", status="idle", last_run="2026-03-26T02:00:00+09:00", next_run="2026-04-02T02:00:00+09:00"),
    JobStatus(job_name="tools-qoo10-ranking-scraper", category="Qoo10", status="success", last_run="2026-04-01T01:00:00+09:00", next_run="2026-04-02T01:00:00+09:00"),
    # Lemon8
    JobStatus(job_name="tools-lemon8-influencer-scraper", category="Lemon8", status="idle", last_run="2026-03-25T02:00:00+09:00", next_run="2026-04-01T02:00:00+09:00"),
    JobStatus(job_name="tools-lemon8-metrics-collector", category="Lemon8", status="success", last_run="2026-04-01T03:00:00+09:00", next_run="2026-04-02T03:00:00+09:00"),
    JobStatus(job_name="tools-lemon8-account-daily-updater", category="Lemon8", status="success", last_run="2026-04-01T05:00:00+09:00", next_run="2026-04-02T05:00:00+09:00"),
    # Buzz Tools
    JobStatus(job_name="tools-buzz-tools-job", category="Buzz Tools", status="running", last_run="2026-04-01T07:00:00+09:00", next_run=None),
    # 営業リード
    JobStatus(job_name="tools-prtimes-scraper", category="営業リード", status="idle", last_run="2026-03-31T08:00:00+09:00", next_run="2026-04-07T08:00:00+09:00"),
    JobStatus(job_name="tools-gbizinfo-scraper", category="営業リード", status="idle", last_run="2026-03-25T08:00:00+09:00", next_run="2026-04-01T08:00:00+09:00"),
    JobStatus(job_name="tools-rakuten-scraper", category="営業リード", status="idle", last_run="2026-03-31T09:00:00+09:00", next_run="2026-04-07T09:00:00+09:00"),
    JobStatus(job_name="tools-yahoo-shopping-scraper", category="営業リード", status="success", last_run="2026-03-25T09:00:00+09:00", next_run="2026-04-01T09:00:00+09:00"),
    JobStatus(job_name="tools-amazon-scraper", category="営業リード", status="idle", last_run="2026-03-31T10:00:00+09:00", next_run="2026-04-07T10:00:00+09:00"),
    JobStatus(job_name="tools-google-maps-scraper", category="営業リード", status="success", last_run="2026-03-25T10:00:00+09:00", next_run="2026-04-01T10:00:00+09:00"),
    JobStatus(job_name="tools-youtube-leads-scraper", category="営業リード", status="idle", last_run="2026-03-31T11:00:00+09:00", next_run="2026-04-07T11:00:00+09:00"),
    JobStatus(job_name="tools-makuake-scraper", category="営業リード", status="success", last_run="2026-03-25T11:00:00+09:00", next_run="2026-04-01T11:00:00+09:00"),
    JobStatus(job_name="tools-hotpepper-scraper", category="営業リード", status="success", last_run="2026-03-26T08:00:00+09:00", next_run="2026-04-02T08:00:00+09:00"),
    JobStatus(job_name="tools-base-ec-scraper", category="営業リード", status="idle", last_run="2026-03-26T09:00:00+09:00", next_run="2026-04-02T09:00:00+09:00"),
    JobStatus(job_name="tools-campfire-scraper", category="営業リード", status="failed", last_run="2026-03-26T10:00:00+09:00", next_run="2026-04-02T10:00:00+09:00"),
    JobStatus(job_name="tools-migrate-to-sales-leads", category="営業リード", status="success", last_run="2026-04-01T00:00:00+09:00", next_run="2026-05-01T00:00:00+09:00"),
    JobStatus(job_name="tools-cosme-scraper", category="営業リード", status="idle", last_run="2026-03-27T08:00:00+09:00", next_run="2026-04-03T08:00:00+09:00"),
    JobStatus(job_name="tools-itownpage-scraper", category="営業リード", status="success", last_run="2026-03-27T09:00:00+09:00", next_run="2026-04-03T09:00:00+09:00"),
    JobStatus(job_name="tools-minne-scraper", category="営業リード", status="idle", last_run="2026-03-27T10:00:00+09:00", next_run="2026-04-03T10:00:00+09:00"),
    JobStatus(job_name="tools-tabelog-scraper", category="営業リード", status="success", last_run="2026-03-28T08:00:00+09:00", next_run="2026-04-04T08:00:00+09:00"),
    JobStatus(job_name="tools-wantedly-scraper", category="営業リード", status="idle", last_run="2026-03-28T09:00:00+09:00", next_run="2026-04-04T09:00:00+09:00"),
]


@router.get("/jobs", response_model=list[JobStatus])
def get_jobs():
    return MOCK_JOBS
