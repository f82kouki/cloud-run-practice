from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, dashboard, students, scouts

app = FastAPI(title="Scout Platform API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(dashboard.router, prefix="/api")
app.include_router(students.router, prefix="/api")
app.include_router(scouts.router, prefix="/api")
