from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, metrics, jobs


def create_app() -> FastAPI:
    app = FastAPI(title="Cloud Run Practice API", version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(health.router)
    app.include_router(metrics.router, prefix="/api")
    app.include_router(jobs.router, prefix="/api")

    return app
