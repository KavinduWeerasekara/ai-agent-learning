#main.py

import argparse
from src.agent import agent_answer, agent_answer_json, parallel_search, parallel_search_json
import json


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description = "A tiny rule based agent (learning edition)"
    )

    #positonal question (optional).  If if omitted we default to 'hello'

    parser.add_argument("question", nargs="*", help="Your question to the agent")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print debug info about what the agent is doing")
    parser.add_argument("--count", "-c", type=int, default=3, help="Number of results to return for search queries (default: 3)")
    parser.add_argument("--json", action="store_true",help="Output structured JSON instead of text (for search results)")
    parser.add_argument("--async", dest="use_async", action="store_true", help="Use async httpx path where available")
    parser.add_argument("--multi", type=str, default="", help='Run multiple queries separated by ";", e.g. --multi "python;golang;rust"')
    parser.add_argument("--provider", "-p", choices=["fakeA", "fakeB", "searxng", "brave"], default="fakeA", help="Which provider to use")


    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    question = " ".join(args.question) if args.question else "hello"

    # If --multi provided, turn into a list (strip spaces, drop empties)
    queries = [q.strip() for q in args.multi.split(";")] if args.multi else []
    queries = [q for q in queries if q]

    if queries:
        # MULTI-MODE
        if not args.json:
            print(
                parallel_search(
                    queries=queries,
                    verbose=args.verbose,
                    count=args.count,
                    provider=args.provider,
                    use_async=args.use_async,
                )
            )
        else:
            data = parallel_search_json(
                queries=queries,
                verbose=args.verbose,
                count=args.count,
                provider=args.provider,
                use_async=args.use_async,
            )
            print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        # SINGLE-QUERY MODE (existing behavior)
        if not args.json:
            print(
                agent_answer(
                    question,
                    verbose=args.verbose,
                    count=args.count,
                    provider=args.provider,
                    use_async=args.use_async,
                )
            )
        else:
            data = agent_answer_json(
                question,
                verbose=args.verbose,
                count=args.count,
                provider=args.provider,
                use_async=args.use_async,
            )
            print(json.dumps(data, indent=2, ensure_ascii=False))