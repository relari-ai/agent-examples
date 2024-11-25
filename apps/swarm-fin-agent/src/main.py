import sys
import warnings
from typing import Any, Dict

from swarm import Swarm
from agents import supervisor_agent

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

client = Swarm()


def run(query: str) -> str:
    """
    Run the financial agents with a specific query and return the response.

    Args:
        query (str): The user query.

    Returns:
        str: The full response from the agent.
    """
    try:
        print("Supervisor agent running query.")
        response = client.run(
            agent=supervisor_agent,
            messages=[{"role": "user", "content": query}],
            debug=False
        )
        return response.messages[-1]['content']
    except Exception as e:
        print(f"An error occurred while processing the query: {e}")
        return str(e)


def interactive_mode():
    """
    Run in interactive mode, allowing users to ask multiple questions and
    display the complete response.
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
