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
    """
    if not jobs:
        return []

    # Prepare search tokens
    role_clean = re.sub(r'[^\w\s]', '', role.lower())
    role_tokens = set(role_clean.split())
    
    # Define synonyms/aliases to broaden search
    synonyms = {
        'engineer': {'developer', 'programmer', 'coder', 'architect'},
        'developer': {'engineer', 'programmer', 'coder', 'architect'},
        'manager': {'lead', 'director', 'head', 'vp'},
        'admin': {'administrator', 'coordinator'},
        'administrator': {'admin', 'coordinator'},
        'designer': {'artist', 'creative'},
    }
    
    # Expand role tokens with synonyms
    expanded_role_tokens = set(role_tokens)
    for token in role_tokens:
        if token in synonyms:
            expanded_role_tokens.update(synonyms[token])

    filtered_jobs = []
    
    # Common stop words to ignore in strict matching (optional, but 'senior' is distinct from 'software')
    # We generally want to match content words.
    
    for job in jobs:
        title = job.get('title', '')
        if not title or title == "N/A":
            continue
            
        title_clean = re.sub(r'[^\w\s]', '', title.lower())
        title_tokens = set(title_clean.split())
        
        # Check overlap
        # We require at least ONE significant content word from the role to appear in the title.
        # If the role is multi-word (e.g. "Software Engineer"), we want at least one of them.
        
        overlap = expanded_role_tokens.intersection(title_tokens)
        
        if len(overlap) > 0:
            filtered_jobs.append(job)
            
    return filtered_jobs
