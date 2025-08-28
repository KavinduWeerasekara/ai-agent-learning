import os
from dotenv import load_dotenv

#load environment variables from .env file
load_dotenv()

def agent_answer(question: str, verbose: bool) -> str:
    
    q = question.lower()

    if verbose:
        print("[debug] normalized question ->", q)
    
    if "python" in q:
        return "python is a programming language that is easy to learn"
    
    elif "ai" in q or "artificial" in q:
        return "AI means artificial intelligence: machine that can perform tasks that requring intelligence"

    else:
        # use value from .env instead of hardcoding
        return os.getenv("DEFAULT_ANSWER", "Sorry, I don't know yet.")
