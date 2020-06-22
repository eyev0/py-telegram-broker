def validate_postal_code(postal_code: str) -> int:
    try:
        if len(postal_code) != 6:
            raise ValueError
        result = int(postal_code)
    except ValueError:
        return -1
    return result
