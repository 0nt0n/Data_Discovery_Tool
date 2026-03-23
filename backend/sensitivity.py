

SENSITIVE_PATTERNS = [
    'email', 'phone', 'id', 'age', 
    'income', 'name', 'address', 'birth',
    'password', 'ssn', 'credit', 'salary'
]


def is_sensitive(column_name: str) -> bool:
    name = column_name.lower()
    return any(pat in name for pat in SENSITIVE_PATTERNS)

