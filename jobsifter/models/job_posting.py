"""Data models for job postings and related entities."""

from typing import Optional, Literal
from dataclasses import dataclass

@dataclass
class Salary:
    """Represents a salary of a job posting."""
    amount: float
    currency: str = "USD"
    period: Literal['hourly', 'yearly'] = "yearly"

@dataclass
class Location:
    """Represents a location of a job posting."""
    city: Optional[str]
    state: Optional[str]
    country: str

@dataclass
class JobPosting:
    """Represents a job posting that was approved during processing."""
    title: str
    description: str
    company: str
    location: Location
    salary: Salary
    employment_type: str
    posting_date: str
    company_type: str
    language: Literal['English', 'French']
    remote: bool

@dataclass
class RejectedJob:
    """Represents a job posting that was rejected during processing."""
    raw_data: dict
    reasons: list[str]


# *note:
# dataclass is a class that is used to create a new class from a dictionary.
# it gives us:
# - Auto constructor
# - Default values
# - __repr__, __eq__, etc.


# NOTE: do internships count as full time ever? if they met the salary requirements, would they be considered full time?

# NOTE: 
# should we parse posting_date and make it a datetime object?