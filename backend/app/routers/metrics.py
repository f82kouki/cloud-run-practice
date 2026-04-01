from fastapi import APIRouter
from app.models import PlatformMetrics

router = APIRouter()

MOCK_METRICS = [
    PlatformMetrics(
        platform="Instagram",
        followers=125_400,
        posts=342,
        engagement_rate=3.8,
        collected_at="2026-04-01T03:00:00+09:00",
    ),
    PlatformMetrics(
        platform="YouTube",
        followers=87_200,
        posts=128,
        engagement_rate=5.2,
        collected_at="2026-04-01T04:00:00+09:00",
    ),
    PlatformMetrics(
        platform="Lemon8",
        followers=43_100,
        posts=215,
        engagement_rate=6.1,
        collected_at="2026-04-01T03:00:00+09:00",
    ),
    PlatformMetrics(
        platform="Qoo10",
        followers=0,
        posts=1_820,
        engagement_rate=0.0,
        collected_at="2026-04-01T01:00:00+09:00",
    ),
]


@router.get("/metrics", response_model=list[PlatformMetrics])
def get_metrics():
    return MOCK_METRICS
