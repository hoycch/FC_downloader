def parse_phone(phone: str | int | None) -> tuple[str | None, str]:
    """
    Parse a phone number according to the original Power Query rules.
    
    Returns:
        (country_code, national_number)  e.g. ("65", "91234567")
        or (None, original_phone) when no rule matches.
    """
    if phone is None:
        return None, ""

    original = str(phone).strip()
    # Keep only digits
    clean = "".join(c for c in original if c.isdigit())
    length = len(clean)

    # Case 1: 10 digits starting with 65 or 82
    if length == 10 and clean.startswith(("65", "82")):
        country = clean[:2]
        national = clean[2:]
        return country, national

    # Case 2: 11 digits
    if length == 11:
        # Macau 853
        if clean.startswith("853"):
            return "853", clean[3:]

        # Korea – leading 0 → replace with 82
        if clean.startswith("0"):
            return "82", clean

        # China – starts with 1
        if clean.startswith("1"):
            return "86", clean

    # Fallback – could not parse
    return None, original

