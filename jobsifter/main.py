"""Main module for processing job feed files and managing job postings."""

import sys
import re
from typing import Any

import json
from jobsifter.models import JobPosting, RejectedJob
from jobsifter.ingestion import parse_job
from jobsifter.approval import evaluate_job
from jobsifter.storage import store_approved_jobs, log_approved_jobs,log_rejected_jobs


def safe_load_json_array(file_path: str) -> list[dict[str, Any]]:
    """Attempt to load a valid JSON array 
    even if the file has trailing garbage 
    after the closing bracket."""

    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()

    #  Try to find the last closing bracket (end of JSON array)
    match = re.search(r'\][^\]]*$', text)

    if match:
        # Extract the valid JSON array
        valid_json_text = text[:match.start() + 1]
    else:
        # use the whole file if no closing bracket followed by more text found
        valid_json_text = text 

    try:
        return json.loads(valid_json_text)
    except json.JSONDecodeError as e:
        print(f"❌ Failed to parse JSON file: {file_path}")
        print(f"    Error: {str(e)}")
        raise ValueError(f"JSON decode error: {str(e)}") from e


def run(feed_path: str) -> tuple[list[JobPosting], list[RejectedJob]]:
    """Process a job feed file and return approved and rejected jobs."""
    approved = []
    rejected = []

    try:
        raw_feed = safe_load_json_array(feed_path)
    except ValueError as e:
        print(f"❌ Failed to parse JSON file: {feed_path}")
        print(f"    Error: {str(e)}")
        return [], [RejectedJob(
            raw_data={"feed_path": feed_path},
            reasons=[f"JSON decode error: {str(e)}"]
        )]
    for raw_job in raw_feed:
        try:
            job = parse_job(raw_job)   # returns a JobPosting object
            is_approved, reasons = evaluate_job(job)

            if is_approved:
                approved.append(job)
            else:
                rejected.append(RejectedJob(raw_data=raw_job, reasons=reasons))
        except ValueError as e:
            rejected.append(RejectedJob(raw_data=raw_job, reasons=[f"Parsing error: {str(e)}"]))

    return approved, rejected


if __name__ == "__main__":
    # Allow user to specify a feed file as a command-line argument
    input_feed_path = sys.argv[1] if len(sys.argv) > 1 else "data/feed1.json"

    approved_jobs, rejected_jobs = run(input_feed_path)

    store_approved_jobs(approved_jobs)
    log_approved_jobs(approved_jobs)
    log_rejected_jobs(rejected_jobs)

    print(f"\n✅ Approved jobs: {len(approved_jobs)}")
    print(f"❌ Rejected jobs: {len(rejected_jobs)}")
