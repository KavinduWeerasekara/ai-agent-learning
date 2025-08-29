# src/tools.py

import requests

def fake_search_tool_a(query: str, count: int = 3) -> list[str]:
    """
   Fake provider A (default). Returns numbered fake results.
    """

    return [f"[FAKE-A] Result {i} for '{query}'" for i in range(1, count + 1)]


def fake_search_tool_b(query: str, count: int = 3) -> list[str]:
    """
    Fake provider B (alternate). Slightly different formatting so you can see which provider ran.
    """

    return [f"[FAKE-B] Result {i} for '{query}'" for i in range(1, count + 1)]

def searxng_search_sync(base_url: str, query: str, count: int = 3, timeout: int = 20) -> list[str]:
    """
    Real SearXNG HTTP call (sync). Returns up to `count` display strings.
    """
    try:
        url = base_url.rstrip("/") + "/search"
        params = {"q": query, "format": "json"}
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        return [f"[SEARXNG] Network error: {e}"]
    except ValueError:
        return ["[SEARXNG] Error parsing JSON response"]

    results = []
    for item in data.get("results", [])[:count]:
        title = item.get("title", "No title")
        link = item.get("url", "No URL")
        snippet = item.get("content") or item.get("description") or ""
        results.append(f"[SEARXNG] {title}\n  {link}\n  {snippet}")
    return results or ["[SEARXNG] No results."]
