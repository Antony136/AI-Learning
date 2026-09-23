import re


def normalize_query(query: str) -> str:
    """
    Clean up superficial formatting noise
    without changing the meaning of the query.
    """

    query = query.strip()

    query = re.sub(
        r"\s+",
        " ",
        query
    )

    query = query.lower()

    query = re.sub(
        r"\?{2,}",
        "?",
        query
    )

    query = re.sub(
        r"!{2,}",
        "!",
        query
    )

    return query