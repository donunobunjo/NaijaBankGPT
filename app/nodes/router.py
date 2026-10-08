import re


# Keywords that strongly suggest a banking-related query.
BANKING_KEYWORDS = [
    "bank",
    "account",
    "balance",
    "transfer",
    "transaction",
    "atm",
    "card",
    "cash",
    "payment",
    "deposit",
    "withdraw",
    "withdrawal",
    "loan",
    "credit",
    "debit",
    "pin",
    "money",
    "refund",
    "charge",
    "charged",
    "fee",
    "fraud",
    "cashback",
    "beneficiary",
    "beneficiary",
    "statement",
    "wire",
    "exchange",
    "currency",
]


def banking_router(query: str) -> dict:
    """
    Determine whether a user query is likely to be banking-related.

    This is a lightweight routing layer. It does not determine
    the specific banking intent.
    """

    if not query or not query.strip():
        return {
            "is_banking": False,
            "banking_reason": "Empty query.",
        }

    query_lower = query.lower()

    matched_keywords = [
        keyword
        for keyword in BANKING_KEYWORDS
        if re.search(rf"\b{re.escape(keyword)}\b", query_lower)
    ]

    if matched_keywords:
        return {
            "is_banking": True,
            "banking_reason": (
                f"Banking-related keywords detected: "
                f"{', '.join(matched_keywords)}"
            ),
        }

    return {
        "is_banking": False,
        "banking_reason": "No strong banking-related keywords detected.",
    }