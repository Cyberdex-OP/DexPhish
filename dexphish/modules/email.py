"""Simple email helper (placeholder). Does NOT send real email in this template."""

def send_email(to: str, subject: str, body: str) -> bool:
    """Log the email parameters and return True (placeholder).

    This is intentionally benign and does not perform network operations.
    """
    print(f"[email] to={to!r}, subject={subject!r}, body_len={len(body)}")
    return True
