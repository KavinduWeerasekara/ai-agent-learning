# src/agent.py
import os
from typing import List
from dotenv import load_dotenv
from src.tools import fake_search_tool_a, fake_search_tool_b, searxng_search_sync
from src.models import SearchResult

load_dotenv()

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

def agent_answer(question: str, verbose: bool = False, count: int = 3, provider: str = "fakeA") -> str:
    q = question.lower()
    if verbose:
        print("[debug] normalized question ->", q)
        print("[debug] provider ->", provider)
        print("[debug] count ->", count)

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

def agent_answer_json(question: str, verbose: bool = False, count: int = 3, provider: str = "fakeA"):
    q = question.lower()
    if verbose:
        print("[debug][json] normalized question ->", q)
        print("[debug][json] provider ->", provider)
        print("[debug][json] count ->", count)

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
