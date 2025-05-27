"""Functions for storing and logging job posting results."""

import json
from dataclasses import asdict
from jobsifter.models import JobPosting, RejectedJob

def store_approved_jobs(jobs: list[JobPosting], filename: str = "approved_jobs.json") -> None:
    """Store approved jobs to a JSON file."""
    print(f"Storing {len(jobs)} approved jobs to {filename}")
    job_dicts = [asdict(job) for job in jobs]
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(job_dicts, f, indent=2)

def log_approved_jobs(jobs: list[JobPosting]) -> None:
    """Log approved jobs to the console."""
    print("\n--- Approved Jobs ---")
    for job in jobs:
        title = job.title
        print(f"✅ {title}")
        print(f"{job}")
    print("----------------------\n")

def log_rejected_jobs(jobs: list[RejectedJob]) -> None:
    """Log rejected jobs to the console."""
    print("\n--- Rejected Jobs ---")
    for job in jobs:
        title = job.raw_data.get("title", "[unknown title]")
        print(f"❌ {title}")
        for reason in job.reasons:
            print(f"   - {reason}")
    print("----------------------\n")
