def fake_search_tools(query: str, count: int = 3) -> list[str]:
    """
    A fake search tool that pretends to returj web results. For now, just return a list of made-up answers
    """

    results = []

    for i in range(1, count + 1):
        results.append(f"Result {i} for '{query}' (fake)")

    return results
    