import argparse
from src.agent import agent_answer #import the agent logic
import json
from src.agent import agent_answer_json

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "A tiny rule based agent (learning edition)"
    )

    #positonal question (optional).  If if omitted we default to 'hello'

    parser.add_argument("question", nargs="*", help="Your question to the agent")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print debug info about what the agent is doing")
    parser.add_argument("--count", "-c", type=int, default=3, help="Number of results to return for search queries (default: 3)")
    parser.add_argument("--provider", "-p", type=str, default="fakeA", help="Which provider to use (fakeA, fakeB). Default: fakeA")
    parser.add_argument("--json", action="store_true",help="Output structured JSON instead of text (for search results)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    # join words if user typed multiple tokens without quotes
    question = " ".join(args.question) if args.question else "hello"

    if args.verbose:
        print("[debug] raw args.question ->", args.question)

    if not args.json:
        print(
            agent_answer(
                question,
                verbose=args.verbose,
                count=args.count,
                provider=args.provider,
            )
        )
    else:
        # Step B will make agent_answer_json exist; for now placeholder:
          # we'll add this next
        data = agent_answer_json(
            question,
            verbose=args.verbose,
            count=args.count,
            provider=args.provider,
        )
        print(json.dumps(data, indent=2, ensure_ascii=False))