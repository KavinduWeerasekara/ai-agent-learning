import sys

def agent_answer(question:str) -> str:
    return f"I received your question: {question}"

if __name__ == "__main__":
    q = "".join(sys.argv[1:]) or "hello"
    print(agent_answer(q))