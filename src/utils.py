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
