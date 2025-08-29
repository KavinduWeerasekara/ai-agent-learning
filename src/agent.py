# src/agent.py

import os
from dotenv import load_dotenv
from src.tools import fake_search_tool_a, fake_search_tool_b, searxng_search_sync

#load environment variables from .env file
load_dotenv()

def agent_answer(question: str, verbose: bool, count: int = 3,  provider: str = "fakeA") -> str:

    """Rule-based agent that can call different 'providers' (fake for now)."""
    
    q = question.lower()

    if verbose:
        print("[debug] normalized question ->", q)
        print("[debug] provider ->", provider)
        print("[debug] count ->", count)


    # Simple rule replies

    if "python" in q:
        return "python is a programming language that is easy to learn"
    
    elif "ai" in q or "artificial" in q:
        return "AI means artificial intelligence: machine that can perform tasks that requring intelligence"

    elif "search" in q:
        provider = provider.lower()
        if provider in ("fakea", "fake"):
            results = fake_search_tool_a(q, count=count)
        elif provider in ("fakeb", "fake"):
            results = fake_search_tool_b(q, count=count)
        elif provider in ("searxng", "sx"):
            base = os.getenv("SEARXNG_BASE_URL")
            if not base:
                return "SEARXNG_BASE_URL is not set in .env"
            results = searxng_search_sync(base, q, count=count)
        else:
            return f"Unknown provider '{provider}'. Try --provider fakeA, fakeB, or searxng."

        return "\n".join(results)

    else:
        # use value from .env instead of hardcoding
        return os.getenv("DEFAULT_ANSWER", "Sorry, I don't know yet.")

def _normalize_to_objects(strings: list[str], provider: str):
    """
    Convert our current simple string results into structured dicts.
    This keeps tools unchanged while giving JSON shape to the CLI.
    """
    items = []
    for s in strings:
        # Very simple parser: try to split the lines we format in tools
        # Expected patterns (examples):
        #   "[FAKE-A] Result 1 for 'search cars'"
        #   "[SEARXNG] Title\n  URL\n  Snippet"
        lines = s.splitlines()
        title = lines[0].strip() if lines else s
        url = ""
        snippet = ""
        if provider.lower() in ("searxng", "sx") and len(lines) >= 2:
            url = lines[1].strip()
        if provider.lower() in ("searxng", "sx") and len(lines) >= 3:
            snippet = lines[2].strip()
        items.append({
            "title": title,
            "url": url,
            "snippet": snippet,
            "provider": provider,
        })
    return items

def agent_answer_json(
    question: str,
    verbose: bool = False,
    count: int = 3,
    provider: str = "fakeA",
):
    """
    Structured/JSON answer.
    For now we adapt from the existing text-producing tools by normalizing
    their outputs; later we’ll make tools return structured objects directly.
    """
    q = question.lower()
    if verbose:
        print("[debug][json] normalized question ->", q)
        print("[debug][json] provider ->", provider)
        print("[debug][json] count ->", count)

    # Return a simple structure when it's not a 'search' request
    if "search" not in q:
        return {
            "ok": True,
            "mode": "non-search",
            "answer": agent_answer(question, verbose=verbose, count=count, provider=provider),
        }

    prov = provider.lower()
    if prov in ("fakea", "fake"):
        strings = fake_search_tool_a(q, count=count)
        return {"ok": True, "mode": "search", "items": _normalize_to_objects(strings, provider="fakeA")}
    elif prov in ("fakeb",):
        strings = fake_search_tool_b(q, count=count)
        return {"ok": True, "mode": "search", "items": _normalize_to_objects(strings, provider="fakeB")}
    elif prov in ("searxng", "sx"):
        base = os.getenv("SEARXNG_BASE_URL")
        if not base:
            return {"ok": False, "error": "SEARXNG_BASE_URL is not set in .env"}
        strings = searxng_search_sync(base, q, count=count)
        return {"ok": True, "mode": "search", "items": _normalize_to_objects(strings, provider="searxng")}
    else:
        return {"ok": False, "error": f"Unknown provider '{provider}'"}