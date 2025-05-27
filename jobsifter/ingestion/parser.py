"""Module for parsing raw job data into structured JobPosting objects."""

from typing import Any, Dict
from jobsifter.models import JobPosting, Salary, Location

def parse_job(raw_job: Dict[str, Any]) -> JobPosting:
    """Convert raw job data into a structured JobPosting object."""
    try:
        # Salary — normalize from dict or number
        salary_raw = raw_job.get("salary")

        if isinstance(salary_raw, dict):
            amount = float(salary_raw.get("value", 0))
            currency = salary_raw.get("currency", "USD")
            period = salary_raw.get("unit") or ("hourly" if amount < 200 else "yearly")
        else:
            amount = float(salary_raw)
            currency = "USD"
            period = "hourly" if amount < 200 else "yearly"

        salary = Salary(amount=amount, currency=currency, period=period)

        # Location — normalize from dict or string
        location_raw = raw_job.get("location")
        if isinstance(location_raw, dict):
            location = Location(
                city = location_raw.get("city"),
                state = location_raw.get("state"),
                country = location_raw.get("country")
            )
        elif isinstance(location_raw, str):
            parts = [p.strip() for p in location_raw.split(",")]
            city = parts[0] if len(parts) > 2 else None
            state = parts[1] if len(parts) > 1 else None
            country = parts[-1]
            location = Location(city=city, state=state, country=country)
        else:
            raise ValueError(f"Invalid location format: {location_raw}")

        # Posting date — we may make this a datetime object later
        posting_date = raw_job.get("posting_date")

        return JobPosting(
            title=raw_job.get("title"),
            description=raw_job.get("description"),
            company=raw_job.get("company"),
            location=location,
            salary=salary,
            employment_type=raw_job.get("employment_type"),
            posting_date=posting_date,
            remote=raw_job.get("remote", False),
            company_type=raw_job.get("company_type"),
            language = raw_job.get("language") or "English"
        )
        # NOTE: do we want to reject the job that dont have a 
        # language listed? or can we assume they are English if not?

    except Exception as e:
        raise ValueError(f"Error parsing job: {str(e)}") from e
