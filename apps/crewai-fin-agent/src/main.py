#!/usr/bin/env python
import sys
import warnings
from typing import Dict, Any

from crew import CrewaiFinAgent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run(query: str) -> str:
    """
    Run the crew with a specific query.
    """
    try:
        inputs = {'query': query}
        return CrewaiFinAgent().crew().kickoff(inputs=inputs)
    except Exception as e:
        print(f"An error occurred while running the crew: {e}")
        return str(e)

def interactive_mode():
    """
    Run the crew in interactive mode, allowing users to ask multiple questions.
    """
    print("Welcome to the Financial Assistant!")
    print("You can ask questions about stocks, companies, and financial data.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Your question: ").strip()
        if query.lower() in ['exit', 'quit']:
            print("Thank you for using the Financial Assistant. Goodbye!")
            break
        
        print("\nProcessing your request...\n")
        response = run(query)
        print(f"Response: {response}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # If command line argument is provided, use it as the query
        query = " ".join(sys.argv[1:])
        print(run(query))
    else:
        # If no arguments, run in interactive mode
        interactive_mode()
