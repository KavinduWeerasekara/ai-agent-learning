#main.py

import json
from src.agent_runtime import run_agent
import os
import asyncio
from dotenv import load_dotenv


async def main():
    """
    Run the command-line interface for the web search agent.
    """
    # Load environment variables
    load_dotenv(override=True)
    
    print("Web Search Agent CLI")
    print("--------------------")
    print("Type 'exit' or 'quit' to exit the program.")
    print("Type 'help' for help.")
    print()
    
    # Get the search provider information
    brave_api_key = os.getenv("BRAVE_API_KEY")
    searxng_base_url = os.getenv("SEARXNG_BASE_URL")
    search_provider = ""
    
    if brave_api_key:
        print(f"Using Brave Search API for web searches")
        search_provider = "brave"
    elif searxng_base_url:
        print(f"Using SearXNG at {searxng_base_url} for web searches")
        search_provider = "searxng"
    else:
        print("Warning: No search provider configured. Please set either BRAVE_API_KEY or SEARXNG_BASE_URL environment variable.")
    
    print()
    
    while True:
        try:
            # Get user input
            user_input = input("Enter your search query: ")
            
            # Check if the user wants to exit
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            # Check if the user wants help
            if user_input.lower() == "help":
                print("\nHelp:")
                print("  - Enter a search query to search the web")
                print("  - Type 'exit' or 'quit' to exit the program")
                print("  - Type 'help' for this help message")
                print()
                continue
                
            # Run the agent
            print("\nSearching...")
            data = await run_agent(user_input, provider=search_provider, count=3)
            response = json.dumps(data, indent=2, ensure_ascii=False)
            
            # Print the response
            print("\nResponse:")
            print(response)
            print()
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            print()

if __name__ == "__main__":
    asyncio.run(main())
    