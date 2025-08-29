import requests
from typing import List
from src.models import SearchResult

def fake_search_tool_a(query: str, count: int = 3) -> list[str]:
    return [f"[FAKE-A] Result {i} for '{query}'" for i in range(1, count + 1)]

def fake_search_tool_b(query: str, count: int = 3) -> list[str]:
    return [f"[FAKE-B] ({i}/{count}) -> '{query}'" for i in range(1, count + 1)]

def searxng_search_sync(base_url: str, query: str, count: int = 3, timeout: int = 20) -> List[SearchResult]:
    """
    Real SearXNG HTTP call (sync). Returns Pydantic SearchResult objects.
    """
    try:
        url = base_url.rstrip("/") + "/search"
        params = {"q": query, "format": "json"}
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        # Return one 'error-flavored' item; keeps types consistent
        return [SearchResult(title=f"[SEARXNG] Network error: {e}", url="", snippet="", provider="searxng")]
    except ValueError:
        return [SearchResult(title="[SEARXNG] Error parsing JSON response", url="", snippet="", provider="searxng")]

    items: List[SearchResult] = []
    for item in data.get("results", [])[:count]:
        items.append(
            SearchResult(
                title=item.get("title", "No title"),
                url=item.get("url", "") or "",
                snippet=item.get("content") or item.get("description") or "",
                provider="searxng",
            )
        )
    return items or [SearchResult(title="[SEARXNG] No results.", url="", snippet="", provider="searxng")]
