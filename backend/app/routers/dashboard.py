from fastapi import APIRouter
from app.models import DashboardStats

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
def get_dashboard():
    return DashboardStats(
        total_scouts_sent=1842,
        scouts_opened=1290,
        scouts_accepted=387,
        scouts_declined=215,
        open_rate=70.0,
        accept_rate=30.0,
        active_students=12460,
        new_students_this_week=328,
    )
