from pydantic import BaseModel, HttpUrl
from typing import Literal, Optional

class SearchResult(BaseModel):
    title: str
    url: Optional[str] = ""     # keep str since fake tools may not have URLs yet
    snippet: Optional[str] = ""
    provider: Literal["fakeA", "fakeB", "searxng", "brave"]
