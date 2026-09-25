import re

HIGH_RISK_PATTERNS = [
    r"\bi\s*want\s*to\s*die\b",
    r"\bi\s*want\s*to\s*kill\s*my\s*self\b",
    r"\bi\s*will\s*kill\s*my\s*self\b",
    r"\bkill\s*my\s*self\b",
    r"\bend\s*my\s*life\b",
    r"\bi\s*don'?t\s*want\s*to\s*live\b",
    r"\bi\s*want\s*to\s*end\s*my\s*life\b",
    r"\bsuicide\b",
    r"\bsuicidal\b",
    r"\bself[\s-]*harm\b",
]

def check_safety(text):
    text = text.lower().strip()

    # Remove spaces/hyphens inside "my self" / "my-self"
    normalized_text = re.sub(r"my[\s-]+self", "myself", text)

    for pattern in HIGH_RISK_PATTERNS:
        if re.search(pattern, text) or re.search(pattern, normalized_text):
            return True

    return False