import sys
import asyncio
from typing import List
from tqdm.asyncio import tqdm as async_tqdm
from langchain_core.messages import HumanMessage

from graph import build_app

async def run(app, query: str, config: dict):
    """Process a single query and return the assistant's response.

    Args:
        app: The application instance.
        query (str): The user's query.
        config (dict): Configuration for the query, including thread information.
    """
    inputs = {"messages": [HumanMessage(content=query)]}
    async for chunk in app.astream(inputs, config, stream_mode="values"):
        chunk["messages"][-1].pretty_print()

async def interactive_mode(app):
    """Start an interactive session with the Finance Assistant."""
    print("Welcome to the Financial Assistant powered by LangGraph agents!")
    print("You can ask questions about stocks, companies, and financial data.")
    print("The assistant has access to public company data and can browse the web for more information if needed.")
    print("Type 'exit' to end the session.")

    # Initialize the memory config for the interactive session
    config = {"configurable": {"thread_id": "1"}}

    while True:
        query = input("\nYour question: ").strip()
        if query.lower() == 'exit':
            print("Thank you for using the Finance Assistant. Goodbye!")
            break

        print("Processing your request...")
        await run(app, query, config)
        print("\nResponse complete.")

async def main():
    """Main entry point for the application."""
    app = build_app()
    
    # Uncomment to print the graph
    # print(app.get_graph().draw_mermaid())
    
    if len(sys.argv) < 2:
        await interactive_mode(app)
    else:
        query = " ".join(sys.argv[1:])
        # Initialize memory config for single query if needed
        config = {"configurable": {"thread_id": "1"}}
        await run(app, query, config)

if __name__ == '__main__':
    asyncio.run(main())
