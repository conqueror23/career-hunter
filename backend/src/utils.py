"""Utility functions for job filtering and salary parsing."""

import re
from functools import lru_cache
from typing import Any, Dict, FrozenSet, List, Tuple

try:
    from .config import JOB_SYNONYMS, STOP_WORDS
except ImportError:
    from config import JOB_SYNONYMS, STOP_WORDS

# Pre-compile regex patterns for better performance
_NON_WORD_PATTERN = re.compile(r"[^\w\s]")

# Pre-compile work type patterns for O(1) lookup instead of O(n) string search
_WORK_TYPE_PATTERNS = {
    "remote": re.compile(r"\b(remote|work\s*from\s*home|wfh)\b", re.IGNORECASE),
    "hybrid": re.compile(r"\bhybrid\b", re.IGNORECASE),
}


def parse_salary(salary_str: str) -> Tuple[int, int]:
    """
    Parse salary range string like '140k-200k' or '140000-200000'.

    Args:
        salary_str: Salary range in format 'min-max'

    Returns:
        Tuple of (min_salary, max_salary)

    Raises:
        ValueError: If salary format is invalid
    """
    clean_str = salary_str.replace(",", "").replace(" ", "").lower()
    parts = clean_str.split("-")

    if len(parts) != 2:
        raise ValueError("Salary must be in format 'min-max' (e.g. 140k-200k)")

    def convert_num(s: str) -> int:
        if "k" in s:
            return int(float(s.replace("k", "")) * 1000)
        return int(s)

    try:
        min_sal = convert_num(parts[0])
        max_sal = convert_num(parts[1])
        return min_sal, max_sal
    except ValueError:
        raise ValueError("Invalid salary number format")


@lru_cache(maxsize=256)
def _get_matching_tokens(role_token: str) -> FrozenSet[str]:
    """Get all tokens that should match for a given role token (including synonyms).

    Uses lru_cache for O(1) lookup after first computation.
    Returns FrozenSet for hashability and immutability.
    """
    possible_matches = {role_token}

    # Add synonyms if the token is a key
    if role_token in JOB_SYNONYMS:
        possible_matches.update(JOB_SYNONYMS[role_token])

    # Check if any synonym maps to this token
    for key, syn_set in JOB_SYNONYMS.items():
        if role_token in syn_set:
            possible_matches.add(key)
            possible_matches.update(syn_set)

    return frozenset(possible_matches)


def filter_jobs(jobs: List[Dict[str, Any]], role: str) -> List[Dict[str, Any]]:
    """
    Filter jobs based on title relevance to the search role.

    All significant words from the role must match (with synonyms allowed).

    Args:
        jobs: List of job dictionaries
        role: Search role string

    Returns:
        Filtered list of jobs matching the role
    """
    if not jobs:
        return []

    # Tokenize and clean role (using pre-compiled pattern)
    role_clean = _NON_WORD_PATTERN.sub("", role.lower())
    role_tokens = [t for t in role_clean.split() if t]

    # Filter out stop words
    significant_tokens = [t for t in role_tokens if t not in STOP_WORDS]
    if not significant_tokens:
        significant_tokens = role_tokens

    filtered_jobs = []

    for job in jobs:
        title = job.get("title", "")
        if not title or title == "N/A":
            continue

        title_clean = _NON_WORD_PATTERN.sub("", title.lower())
        title_tokens = frozenset(title_clean.split())

        # Check if ALL significant role tokens match
        all_match = True
        for role_token in significant_tokens:
            possible_matches = _get_matching_tokens(role_token)
            if not possible_matches.intersection(title_tokens):
                all_match = False
                break

        if all_match:
            filtered_jobs.append(job)

    return filtered_jobs


def _matches_work_type(text: str, work_type: str) -> bool:
    """Check if text matches work type pattern using pre-compiled regex."""
    pattern = _WORK_TYPE_PATTERNS.get(work_type)
    if pattern is None:
        return False
    return pattern.search(text) is not None


def filter_by_work_type(jobs: List[Dict[str, Any]], work_type: str) -> List[Dict[str, Any]]:
    """
    Filter jobs by work type: all, remote, hybrid, onsite.

    Uses pre-compiled regex patterns for efficient O(n) matching
    instead of O(n*m) substring searches.

    Args:
        jobs: List of job dictionaries
        work_type: Work type filter ('all', 'remote', 'hybrid', 'onsite')

    Returns:
        Filtered list of jobs
    """
    if not jobs or work_type == "all":
        return jobs

    filtered = []

    for job in jobs:
        is_remote = job.get("is_remote", False)
        wfh_type = str(job.get("work_from_home_type", "") or "")
        location = str(job.get("location", "") or "")
        title = str(job.get("title", "") or "")
        description = str(job.get("description", "") or "")

        all_text = f"{wfh_type} {location} {title} {description}"

        if work_type == "remote":
            if is_remote or _matches_work_type(all_text, "remote"):
                filtered.append(job)
        elif work_type == "hybrid":
            if _matches_work_type(all_text, "hybrid"):
                filtered.append(job)
        elif work_type == "onsite":
            is_remote_job = is_remote or _matches_work_type(all_text, "remote")
            is_hybrid_job = _matches_work_type(all_text, "hybrid")
            if not is_remote_job and not is_hybrid_job:
                filtered.append(job)

    return filtered
