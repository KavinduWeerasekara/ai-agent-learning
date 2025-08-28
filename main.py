import argparse
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

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "A tiny rule based agent (learning edition)"
    )

    #positonal question (optional).  If if omitted we default to 'hello'

    parser.add_argument("question", nargs="*", help="Your question to the agent")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print debug info about what the agent is doing")

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # join words if user typed multiple tokens without quotes
    question = " ".join(args.question) if args.question else "hello"

    if args.verbose:
        print("[debug] raw args.question ->", args.question)
        print("[debug] final question string ->", question)

    print(agent_answer(question, verbose=args.verbose))