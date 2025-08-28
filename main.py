import sys

def agent_answer(question:str) -> str:
    
    q = question.lower()
    
    if "python"  in q:
        return "python is a programming language that is easy to learn"
    
    elif "ai"in q or "artificial"  in q:
        return "AI means artificial intelligence: machine that can perform tasks that requring intelligence"

    else:
        return f"Sorry I dont know about '{question}' yet."


if __name__ == "__main__":
    q = "".join(sys.argv[1:]) or "hello"
    print(agent_answer(q))