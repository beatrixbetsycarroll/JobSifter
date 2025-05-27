from jobsifter.models import JobPosting
from jobsifter.constants import ALLOWED_COUNTRIES, MIN_YEARLY_SALARY, MIN_HOURLY_SALARY

def evaluate_job(job: JobPosting) -> tuple[bool, list[str]]:
    """Evaluate a job posting and return a tuple of (is_approved, reasons)"""

    reasons = []

    # 1: Location (most frequent failure reason)
    if not job.remote and job.location.country not in ALLOWED_COUNTRIES:
        reasons.append(f"Job must be remote or in allowed countries, but job is in {job.location.country}")

    # 2: Employment type
    if job.employment_type != "Full-Time":
        reasons.append(f"Job must be full-time, but job is {job.employment_type}")

    # 3: Salary
    is_yearly = job.salary.period == "yearly"
    is_hourly = job.salary.period == "hourly"

    # NOTE: I think the instructions said that it had to be > the min, but i think they maybe meant >= the min?
    if is_yearly and job.salary.amount < MIN_YEARLY_SALARY:
        reasons.append(f"Job is yearly and must have a yearly salary of at least ${MIN_YEARLY_SALARY} ({job.salary.amount} is too low)")
    elif is_hourly and job.salary.amount < MIN_HOURLY_SALARY:
        reasons.append(f"Job is hourly and must have an hourly salary of at least ${MIN_HOURLY_SALARY} ({job.salary.amount} is too low)")
    
    # 4: Company type
    if job.company_type == "Staffing Firm":
        reasons.append("Job must not be from a staffing firm")
    
    # 5: Language
    # NOTE: Spec says "description must be in English (or French if in Canada)" but I think they mean the language must be English, or if it is in Canada it can be in English or French

    if job.language == "English":
        pass
    elif job.language == "French":
        if job.location.country != "Canada":
            reasons.append(f"French-language jobs are only allowed if located in Canada (job is in {job.location.country})")
    else:
        reasons.append(f"Job must be in English, or in French if the job is in Canada (language is {job.language})")


    return len(reasons) == 0, reasons