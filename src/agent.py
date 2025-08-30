# src/agent.py

import os
from typing import List, Dict
from dotenv import load_dotenv
from src.tools import fake_search_tool_a, fake_search_tool_b, searxng_search_sync, searxng_search_async
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

def _render_results_text(items: List[SearchResult]) -> str:
    lines = []
    for it in items:
        block = f"[{it.provider.upper()}] {it.title}"
        if it.url:
            block += f"\n  {it.url}"
        if it.snippet:
            block += f"\n  {it.snippet}"
        lines.append(block)
    return "\n".join(lines)

def agent_answer(question: str, verbose: bool = False, count: int = 3, provider: str = "fakeA", use_async: bool = False) -> str:
    q = question.lower()
    if verbose:
        print("[debug] normalized question ->", q)
        print("[debug] provider ->", provider)
        print("[debug] count ->", count)
        print("[debug] async ->", use_async)

    if "python" in q:
        return "Python is a programming language that is easy to learn."
    elif "ai" in q or "artificial intelligence" in q:
        return "AI means artificial intelligence: machines that can perform tasks requiring intelligence."
    elif "search" in q:
        prov = provider.lower()
        if prov in ("searxng", "sx"):
            base = os.getenv("SEARXNG_BASE_URL")
            if not base:
                return "SEARXNG_BASE_URL is not set in .env"
            if use_async:
                items = asyncio.run(searxng_search_async(base, q, count=count))
            else:
                items = searxng_search_sync(base, q, count=count)
            return _render_results_text(items)
        elif prov in ("fakea", "fake"):
            items = fake_search_tool_a(q, count=count)
            return _render_results_text(items)
        elif prov in ("fakeb",):
            items = fake_search_tool_b(q, count=count)
            return _render_results_text(items)
        else:
            return f"Unknown provider '{provider}'. Try --provider fakeA, fakeB, or searxng."
    return os.getenv("DEFAULT_ANSWER", "Sorry, I don't know yet.")

def agent_answer_json(question: str, verbose: bool = False, count: int = 3, provider: str = "fakeA", use_async: bool = False):
    q = question.lower()
    if verbose:
        print("[debug][json] normalized question ->", q)
        print("[debug][json] provider ->", provider)
        print("[debug][json] count ->", count)
        print("[debug] async ->", use_async)

    if "search" not in q:
        return {
            "ok": True,
            "mode": "non-search",
            "answer": agent_answer(question, verbose=verbose, count=count, provider=provider),
        }

    prov = provider.lower()
    if prov in ("searxng", "sx"):
        base = os.getenv("SEARXNG_BASE_URL")
        if not base:
            return {"ok": False, "error": "SEARXNG_BASE_URL is not set in .env"}
        if use_async:
            items = asyncio.run(searxng_search_async(base, q, count=count))
        else:
            items = searxng_search_sync(base, q, count=count)
        return {"ok": True, "mode": "search", "items": [it.model_dump() for it in items]}
    elif prov in ("fakea", "fake"):
        items = fake_search_tool_a(q, count=count)
        return {"ok": True, "mode": "search", "items": [it.model_dump() for it in items]}
    elif prov in ("fakeb",):
        items = fake_search_tool_b(q, count=count)
        return {"ok": True, "mode": "search", "items": [it.model_dump() for it in items]}
    else:
        return {"ok": False, "error": f"Unknown provider '{provider}'"}

def parallel_search(
    queries: List[str],
    verbose: bool = False,
    count: int = 3,
    provider: str = "fakeA",
    use_async: bool = False,
) -> str:
    """Text-mode: run multiple queries (parallel if async+searxng)."""
    prov = provider.lower()
    if verbose:
        print("[debug][multi] queries ->", queries)
        print("[debug][multi] provider ->", provider)
        print("[debug][multi] count ->", count)
        print("[debug][multi] async ->", use_async)

    results_by_query: Dict[str, List[SearchResult]] = {}

    if prov in ("searxng", "sx"):
        base = os.getenv("SEARXNG_BASE_URL")
        if not base:
            return "SEARXNG_BASE_URL is not set in .env"

        if use_async:
            async def _run_all():
                # launch all requests concurrently
                tasks = [searxng_search_async(base, q, count=count) for q in queries]
                lists = await asyncio.gather(*tasks, return_exceptions=False)
                return lists

            lists = asyncio.run(_run_all())
            for q, items in zip(queries, lists):
                results_by_query[q] = items
        else:
            # sequential fallback
            for q in queries:
                results_by_query[q] = searxng_search_sync(base, q, count=count) 

    elif prov in ("fakea", "fake"):
        for q in queries:
            results_by_query[q] = fake_search_tool_a(q, count=count)

    elif prov in ("fakeb",):
        for q in queries:
            results_by_query[q] = fake_search_tool_b(q, count=count)
    else:
        return f"Unknown provider '{provider}'. Try --provider fakeA, fakeB, or searxng."

    return _render_sectioned_text(results_by_query)

def parallel_search_json(
    queries: List[str],
    verbose: bool = False,
    count: int = 3,
    provider: str = "fakeA",
    use_async: bool = False,
):
    """JSON-mode: run multiple queries (parallel if async+searxng)."""
    prov = provider.lower()
    if verbose:
        print("[debug][multi-json] queries ->", queries)
        print("[debug][multi-json] provider ->", provider)
        print("[debug][multi-json] count ->", count)
        print("[debug][multi-json] async ->", use_async)

    results_by_query: Dict[str, List[SearchResult]] = {}

    if prov in ("searxng", "sx"):
        base = os.getenv("SEARXNG_BASE_URL")
        if not base:
            return {"ok": False, "error": "SEARXNG_BASE_URL is not set in .env"}

        if use_async:
            async def _run_all():
                tasks = [searxng_search_async(base, q, count=count) for q in queries]
                lists = await asyncio.gather(*tasks, return_exceptions=False)
                return lists

            lists = asyncio.run(_run_all())
            for q, items in zip(queries, lists):
                results_by_query[q] = items
        else:
            for q in queries:
                results_by_query[q] = searxng_search_sync(base, q, count=count)

    elif prov in ("fakea", "fake"):
        for q in queries:
            results_by_query[q] = fake_search_tool_a(q, count=count)

    elif prov in ("fakeb",):
        for q in queries:
            results_by_query[q] = fake_search_tool_b(q, count=count)
    else:
        return {"ok": False, "error": f"Unknown provider '{provider}'"}

    # shape: { "ok": true, "mode": "multi-search", "results": { "<query>": [ {...}, {...} ] } }
    return {
        "ok": True,
        "mode": "multi-search",
        "results": {q: [it.model_dump() for it in items] for q, items in results_by_query.items()},
    }