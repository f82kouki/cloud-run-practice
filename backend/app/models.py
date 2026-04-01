from pydantic import BaseModel


class Student(BaseModel):
    id: int
    name: str
    university: str
    faculty: str
    graduation_year: int
    skills: list[str]
    desired_industries: list[str]
    self_pr: str
    last_login: str


class ScoutMessage(BaseModel):
    id: int
    student_id: int
    student_name: str
    student_university: str
    subject: str
    status: str  # "pending" | "opened" | "accepted" | "declined"
    sent_at: str
    responded_at: str | None


class DashboardStats(BaseModel):
    total_scouts_sent: int
    scouts_opened: int
    scouts_accepted: int
    scouts_declined: int
    open_rate: float
    accept_rate: float
    active_students: int
    new_students_this_week: int
