# src/tools.py

import requests
from typing import List
from src.models import SearchResult
import httpx

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
