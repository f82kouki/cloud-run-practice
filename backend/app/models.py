from pydantic import BaseModel


class PlatformMetrics(BaseModel):
    platform: str
    followers: int
    posts: int
    engagement_rate: float
    collected_at: str


class JobStatus(BaseModel):
    job_name: str
    category: str
    status: str  # "success" | "running" | "idle" | "failed"
    last_run: str | None
    next_run: str | None
