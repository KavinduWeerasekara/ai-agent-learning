import os
import asyncio
from dataclasses import dataclass
from typing import List
from pydantic_ai import Agent, RunContext
from src.llm import get_llm_model
from src.prompt import AGENT_SYSTEM_PROMPT
from src.tools import searxng_search_async, brave_search_async
from src.models import SearchResult
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode


agent = Agent(get_llm_model(), system_prompt=AGENT_SYSTEM_PROMPT, retries=0)

@dataclass
class Deps:
    provider: str  # "searxng" | "brave"
    count: int     # number of results per search

def _strip_tracking_params(url: str) -> str:
    try:
        u = urlparse(url)
        # keep only "core" query params, drop common trackers
        drop = {"utm_source", "utm_medium", "utm_campaign", "utm_term", "utm_content", "gclid", "fbclid"}
        q = [(k, v) for k, v in parse_qsl(u.query, keep_blank_values=True) if k.lower() not in drop]
        return urlunparse((u.scheme, u.netloc, u.path, u.params, urlencode(q), u.fragment))
    except Exception:
        return url

def _truncate_snippet(s: str, max_len: int = 400) -> str:
    s = (s or "").strip()
    return (s[: max_len - 1] + "…") if len(s) > max_len else s

def _dedupe_by_location(items: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for it in items:
        url = _strip_tracking_params(it.get("url") or "")
        # make a compact key (domain+path)
        try:
            u = urlparse(url)
            key = (u.netloc.lower(), u.path)
        except Exception:
            key = (url.lower(), "")
        if key in seen:
            continue
        seen.add(key)
        if url:
            it = {**it, "url": url}
        out.append(it)
    return out

@agent.tool
async def web_search(ctx: RunContext[Deps], query: str) -> List[dict]:
    """
    Search the web using the provider in ctx.deps.
    Returns list[dict] with fields (title, url, snippet, provider).
    """
    prov = ctx.deps.provider.lower()

    if prov in ("searxng", "sx"):
        base = os.getenv("SEARXNG_BASE_URL")
        if not base:
            return [{"title": "[SEARXNG] Missing SEARXNG_BASE_URL", "url": "", "snippet": "", "provider": "searxng"}]
        items: List[SearchResult] = await searxng_search_async(base, query, count=ctx.deps.count)
        payload = [{**it, "snippet": _truncate_snippet(it.get("snippet") or "")} for it in [it.model_dump() for it in items]]
        return _dedupe_by_location(payload)

    if prov == "brave":
        api_key = os.getenv("BRAVE_API_KEY")
        if not api_key:
            return [{"title": "[BRAVE] Missing BRAVE_API_KEY", "url": "", "snippet": "", "provider": "brave"}]
        items: List[SearchResult] = await brave_search_async(api_key, query, count=ctx.deps.count)
        payload = [{**it, "snippet": _truncate_snippet(it.get("snippet") or "")} for it in [it.model_dump() for it in items]]
        return _dedupe_by_location(payload)

    return [{"title": f"[agent] Unknown provider '{ctx.deps.provider}'", "url": "", "snippet": "", "provider": prov}]

async def run_agent_async(question: str, provider: str = "searxng", count: int = 3) -> dict:
    """
    Run the LLM agent with access to the `web_search` tool.
    Always returns JSON: {"ok": True, "answer": str}
    """
    deps = Deps(provider=provider, count=count)
    result = await agent.run(question, deps=deps)
    return {"ok": True, "answer": result.output}

def run_agent(question: str, provider: str, count: int) -> dict:
    """
    Sync entry point (wraps the async runner with asyncio.run).
    """
    return asyncio.run(run_agent_async(question, provider, count))
