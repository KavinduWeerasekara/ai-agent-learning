# src/tools.py

def fake_search_tools_a(query: str, count: int = 3) -> list[str]:
    """
   Fake provider A (default). Returns numbered fake results.
    """

    return [f"[FAKE-A] Result {i} for '{query}'" for i in range(1, count + 1)]


def fake_search_tools_b(query: str, count: int = 3) -> list[str]:
    """
    Fake provider B (alternate). Slightly different formatting so you can see which provider ran.
    """

    return [f"[FAKE-B] Result {i} for '{query}'" for i in range(1, count + 1)]

    