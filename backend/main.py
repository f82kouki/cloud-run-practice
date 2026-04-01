import os
import uvicorn


def main():
    job_type = os.environ.get("JOB_TYPE")
    if job_type:
        from jobs.runner import run_job
        run_job(job_type)
    else:
        uvicorn.run(
            "app:app",
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8082)),
            reload=False,
        )


if __name__ == "__main__":
    main()
