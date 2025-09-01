# src/agent.py

import os
from typing import List, Dict
from dotenv import load_dotenv
from src.tools import searxng_search_async, brave_search_async
from src.models import SearchResult
import asyncio

load_dotenv()

def _render_sectioned_text(results_by_query: Dict[str, List[SearchResult]]) -> str:
    """Render multiple queries, each as its own titled section."""
    sections = []
    for q, items in results_by_query.items():
        header = f"=== {q} ==="
        body = _render_results_text(items)
        sections.append(f"{header}\n{body}")
    return "\n\n".join(sections)


def parallel_search_json(
    queries: List[str],
    verbose: bool = False,
    count: int = 3,
    provider: str = "searxng",
):
    """JSON-mode: run multiple queries (parallel if async+searxng)."""
    prov = provider.lower()
    if verbose:
        print("[debug][multi-json] queries ->", queries)
        print("[debug][multi-json] provider ->", provider)
        print("[debug][multi-json] count ->", count)

    results_by_query: Dict[str, List[SearchResult]] = {}

    if prov in ("searxng", "sx"):
        base = os.getenv("SEARXNG_BASE_URL")
        if not base:
            return {"ok": False, "error": "SEARXNG_BASE_URL is not set in .env"}
        
        async def _run_all():
            tasks = [searxng_search_async(base, q, count=count) for q in queries]
            lists = await asyncio.gather(*tasks, return_exceptions=False)
            return lists

        lists = asyncio.run(_run_all())
        for q, items in zip(queries, lists):
            results_by_query[q] = items


    elif prov in ("brave",):
        api_key = os.getenv("BRAVE_API_KEY")
        if not api_key:
            return {"ok": False, "error": "BRAVE_API_KEY is not set in .env"}
        
        async def _run_all():
            tasks = [brave_search_async(api_key, q, count=count) for q in queries]
            lists = await asyncio.gather(*tasks, return_exceptions=False)
            return lists

        lists = asyncio.run(_run_all())
        for q, items in zip(queries, lists):
            results_by_query[q] = items

    else:
        return {"ok": False, "error": f"Unknown provider '{provider}'"}

    # shape: { "ok": true, "mode": "multi-search", "results": { "<query>": [ {...}, {...} ] } }
    return {
        "ok": True,
        "mode": "multi-search",
        "results": {q: [it.model_dump() for it in items] for q, items in results_by_query.items()},
    }