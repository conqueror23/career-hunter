"""Pydantic models for API requests and responses."""

import math
from datetime import date
from typing import Any, Optional, Union

from pydantic import BaseModel, Field, field_serializer, field_validator


def is_nan(value: Any) -> bool:
    """Check if value is NaN or None."""
    if value is None:
        return True
    if isinstance(value, float):
        try:
            return math.isnan(value)
        except (TypeError, ValueError):
            return False
    if isinstance(value, str) and value.lower() == "nan":
        return True
    return False


def clean_value(value: Any) -> Optional[str]:
    """Convert NaN/None values to None, otherwise return string."""
    if is_nan(value):
        return None
    return str(value)


def clean_date(value: Any) -> Optional[Union[str, date]]:
    """Clean date value, converting NaN to None."""
    if is_nan(value):
        return None
    if isinstance(value, date):
        return value
    return str(value) if value else None


class SearchRequest(BaseModel):
    """Request model for job search endpoint."""

    role: str = Field(
        ...,
        description="Job role/title to search for",
        json_schema_extra={"example": "Engineer Manager"},
    )
    country: str = Field(
        default="AU",
        description="Country code (AU, US, UK, NZ, CA, IN, SG)",
        json_schema_extra={"example": "AU"},
    )
    location: str = Field(
        default="Australia",
        description="Location/city to search in",
        json_schema_extra={"example": "Sydney"},
    )
    salary: str = Field(
        ...,
        description="Salary range in format 'min-max' (supports 'k' notation)",
        json_schema_extra={"example": "200k-250k"},
    )
    work_type: str = Field(
        default="all",
        description="Work arrangement filter: 'all', 'remote', 'hybrid', 'onsite'",
        json_schema_extra={"example": "remote"},
    )
    limit: int = Field(
        default=25,
        description="Maximum number of results per source",
        ge=1,
        le=100,
        json_schema_extra={"example": 25},
    )


class Job(BaseModel):
    """Job listing model returned from search."""

    id: str = Field(..., description="Unique job identifier")
    site: str = Field(..., description="Source job board (Seek, LinkedIn, Indeed, Glassdoor)")
    title: str = Field(..., description="Job title")
    company: str = Field(..., description="Company name")
    location: Optional[str] = Field(None, description="Job location")
    date_posted: Optional[Union[str, date]] = Field(None, description="Date the job was posted")
    job_url: str = Field(..., description="Direct URL to the job listing")
    salary_range: Optional[str] = Field(None, description="Salary range if available")
    company_url: Optional[str] = Field(None, description="URL to company profile")
    description: Optional[str] = Field(None, description="Full job description")
    is_remote: Optional[bool] = Field(None, description="Whether the job is remote")
    work_from_home_type: Optional[str] = Field(
        None, description="Work arrangement type (remote, hybrid, etc.)"
    )

    @field_validator(
        "location",
        "company",
        "title",
        "salary_range",
        "company_url",
        "description",
        "work_from_home_type",
        mode="before",
    )
    @classmethod
    def clean_nan_values(cls, v: Any) -> Optional[str]:
        return clean_value(v)

    @field_validator("date_posted", mode="before")
    @classmethod
    def clean_date_posted(cls, v: Any) -> Optional[Union[str, date]]:
        return clean_date(v)

    @field_serializer("date_posted")
    def serialize_date(self, value: Optional[Union[str, date]]) -> Optional[str]:
        if value is None:
            return None
        if isinstance(value, date):
            return value.isoformat()
        return str(value)


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str = Field(..., description="Service status", json_schema_extra={"example": "ok"})
