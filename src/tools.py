# src/tools.py

import requests
from typing import List
from src.models import SearchResult
import httpx

# --- BRAVE: sync ---
def brave_search_sync(
    api_key: str,
    query: str,
    count: int = 3,
    timeout: int = 20,
) -> List[SearchResult]:
    """
    Brave Web Search (sync). Requires BRAVE_API_KEY.
    """
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }
    params = {
        "q": query,
        "count": max(1, min(count, 10)),  # Brave allows small page sizes
        "search_lang": "en",
        "text_decorations": True,
    }
    try:
        r = requests.get(url, headers=headers, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
        return [SearchResult(title=f"[BRAVE] Network error: {e}", url="", snippet="", provider="brave")]
    except ValueError:
        return [SearchResult(title="[BRAVE] Error parsing JSON response", url="", snippet="", provider="brave")]

    items: List[SearchResult] = []
    for res in (data.get("web", {}) or {}).get("results", [])[:count]:
        items.append(
            SearchResult(
                title=res.get("title", "No title"),
                url=res.get("url", "") or "",
                snippet=res.get("description") or "",
                provider="brave",
            )
        )
    return items or [SearchResult(title="[BRAVE] No results.", url="", snippet="", provider="brave")]

# --- BRAVE: async ---
async def brave_search_async(
    api_key: str,
    query: str,
    count: int = 3,
    timeout: int = 20,
) -> List[SearchResult]:
    """
    Brave Web Search (async). Requires BRAVE_API_KEY.
    """
    url = "https://api.search.brave.com/res/v1/web/search"
    headers = {
        "Accept": "application/json",
        "X-Subscription-Token": api_key,
    }
    params = {
        "q": query,
        "count": max(1, min(count, 10)),
        "search_lang": "en",
        "text_decorations": True,
    }
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            r = await client.get(url, headers=headers, params=params)
            r.raise_for_status()
            data = r.json()
    except httpx.HTTPError as e:
        return [SearchResult(title=f"[BRAVE] Network error: {e}", url="", snippet="", provider="brave")]
    except ValueError:
        return [SearchResult(title="[BRAVE] Error parsing JSON response", url="", snippet="", provider="brave")]

    items: List[SearchResult] = []
    for res in (data.get("web", {}) or {}).get("results", [])[:count]:
        items.append(
            SearchResult(
                title=res.get("title", "No title"),
                url=res.get("url", "") or "",
                snippet=res.get("description") or "",
                provider="brave",
            )
        )
    return items or [SearchResult(title="[BRAVE] No results.", url="", snippet="", provider="brave")]

def fake_search_tool_a(query: str, count: int = 3) -> List[SearchResult]:
    return [
        SearchResult(
            title=f"[FAKE-A] Result {i} for '{query}'",
            url="",
            snippet="",
            provider="fakeA",
        )
        for i in range(1, count + 1)
    ]

def fake_search_tool_b(query: str, count: int = 3) -> List[SearchResult]:
    return [
        SearchResult(
            title=f"[FAKE-B] ({i}/{count}) -> '{query}'",
            url="",
            snippet="",
            provider="fakeB",
        )
        for i in range(1, count + 1)
    ]

def searxng_search_sync(base_url: str, query: str, count: int = 3, timeout: int = 20) -> List[SearchResult]:
    try:
        url = base_url.rstrip("/") + "/search"
        params = {"q": query, "format": "json"}
        r = requests.get(url, params=params, timeout=timeout)
        r.raise_for_status()
        data = r.json()
    except requests.exceptions.RequestException as e:
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

async def searxng_search_async(base_url, query, count=3, timeout=20) -> List[SearchResult]:
    url = base_url.rstrip("/") + "/search"
    params = {"q": query, "format": "json"}
    async with httpx.AsyncClient(timeout=timeout) as client:
        r = await client.get(url, params=params)
        r.raise_for_status()
        data = r.json()
    
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
