import re

def parse_salary(salary_str):
    """
    Parses salary range string like '140k-200k' or '140000-200000'
    Returns tuple (min_salary, max_salary)
    """
    # Remove commas and spaces
    clean_str = salary_str.replace(',', '').replace(' ', '').lower()
    
    # Extract numbers
    parts = clean_str.split('-')
    if len(parts) != 2:
        raise ValueError("Salary must be in format 'min-max' (e.g. 140k-200k)")
        
    def convert_num(s):
        if 'k' in s:
            return int(float(s.replace('k', '')) * 1000)
        return int(s)
        
    try:
        min_sal = convert_num(parts[0])
        max_sal = convert_num(parts[1])
        return min_sal, max_sal
    except ValueError:
        raise ValueError("Invalid salary number format")

def filter_jobs(jobs, role):
    """
    Filters jobs based on title relevance to the search role.
    ALL significant words from the role must match (with synonyms allowed).
    """
    if not jobs:
        return []

    # Prepare search tokens
    role_clean = re.sub(r'[^\w\s]', '', role.lower())
    role_tokens = [t for t in role_clean.split() if t]

    # Stop words to ignore (these don't need to match)
    stop_words = {'senior', 'junior', 'mid', 'level', 'the', 'a', 'an', 'and', 'or', 'of', 'for', 'in', 'at'}

    # Filter out stop words from role tokens for matching purposes
    significant_role_tokens = [t for t in role_tokens if t not in stop_words]

    if not significant_role_tokens:
        # If only stop words, use all tokens
        significant_role_tokens = role_tokens

    # Define synonyms/aliases to broaden search
    synonyms = {
        'engineer': {'developer', 'programmer', 'coder', 'architect', 'engineering'},
        'developer': {'engineer', 'programmer', 'coder', 'architect', 'development'},
        'software': {'sw', 'application', 'app'},
        'manager': {'lead', 'director', 'head', 'management'},
        'admin': {'administrator', 'coordinator'},
        'administrator': {'admin', 'coordinator'},
        'designer': {'artist', 'creative', 'design'},
        'data': {'analytics', 'bi'},
        'devops': {'sre', 'platform', 'infrastructure'},
        'frontend': {'front-end', 'ui', 'react', 'angular', 'vue'},
        'backend': {'back-end', 'api', 'server'},
        'fullstack': {'full-stack', 'full'},
    }

    filtered_jobs = []

    for job in jobs:
        title = job.get('title', '')
        if not title or title == "N/A":
            continue

        title_clean = re.sub(r'[^\w\s]', '', title.lower())
        title_tokens = set(title_clean.split())

        # Check if ALL significant role tokens match (directly or via synonym)
        all_match = True
        for role_token in significant_role_tokens:
            # Get possible matches for this token (including synonyms)
            possible_matches = {role_token}
            if role_token in synonyms:
                possible_matches.update(synonyms[role_token])

            # Also check if any synonym maps to this token
            for key, syn_set in synonyms.items():
                if role_token in syn_set:
                    possible_matches.add(key)
                    possible_matches.update(syn_set)

            # Check if any possible match is in the title
            if not possible_matches.intersection(title_tokens):
                all_match = False
                break

        if all_match:
            filtered_jobs.append(job)

    return filtered_jobs
