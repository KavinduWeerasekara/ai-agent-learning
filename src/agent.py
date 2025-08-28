import os
from dotenv import load_dotenv
from src.tools import fake_search_tools_a, fake_search_tools_b

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
            results = fake_search_tools_a(q, count=count)
        elif provider in ("fakeb", "fake"):
            results = fake_search_tools_b(q, count=count)
        else:
            return f"Unknown provider '{provider}'. Try --provider fakeA or --provider fakeB."

        return "\n".join(results)

    else:
        # use value from .env instead of hardcoding
        return os.getenv("DEFAULT_ANSWER", "Sorry, I don't know yet.")
