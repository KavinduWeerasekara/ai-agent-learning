import os
from dotenv import load_dotenv
from src.tools import fake_search_tools # <-- import the tool

#load environment variables from .env file
load_dotenv()

def agent_answer(question: str, verbose: bool, count: int = 3) -> str:
    
    q = question.lower()

    if verbose:
        print("[debug] normalized question ->", q)
    
    if "python" in q:
        return "python is a programming language that is easy to learn"
    
    elif "ai" in q or "artificial" in q:
        return "AI means artificial intelligence: machine that can perform tasks that requring intelligence"

    elif "search" in q:
        # NEW: use our fake search tool
        results = fake_search_tools(q, count=count)
        return "\n".join(results)

    else:
        # use value from .env instead of hardcoding
        return os.getenv("DEFAULT_ANSWER", "Sorry, I don't know yet.")
