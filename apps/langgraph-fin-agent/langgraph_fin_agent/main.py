import argparse
import asyncio
import sys
from typing import Any

from langchain_core.messages import HumanMessage
from relari_otel import Relari
from relari_otel.specifications import Specifications

from .graph import build_app

Relari.init(project_name="langgraph-fin-agent", batch=False)


async def main_interactive():
    """Start an interactive session with the Finance Assistant."""
    print("Welcome to the Financial Assistant powered by LangGraph agents!")
    print("You can ask questions about stocks, companies, and financial data.")
    print(
        "The assistant has access to public company data and can browse the web for more information if needed."
    )
    print("Type 'exit' to end the session.")

    app = build_app()
    config = {"configurable": {"thread_id": "1"}}
    while True:
        query = input("\nYour question: ").strip()
        if query.lower() == "exit":
            print("Thank you for using the Finance Assistant. Goodbye!")
            break
        inputs = {"messages": [HumanMessage(content=query)]}
        with Relari.start_new_sample(scenario_id="interactive-query"):
            async for chunk in app.astream(inputs, config, stream_mode="values"):
                chunk["messages"][-1].pretty_print()
            Relari.set_output(chunk["messages"][-1].content)
        print("=" * 80)


async def main_eval():
    app = build_app()

    async def runnable(data: Any):
        inputs = {"messages": [HumanMessage(content=data)]}
        config = {"configurable": {"thread_id": "1"}}
        async for chunk in app.astream(inputs, config, stream_mode="values"):
            chunk["messages"][-1].pretty_print()
        return chunk["messages"][-1].content

    specs = Specifications.load("specifications.json")
    await Relari.eval_runner(specs=specs, runnable=runnable)


def main():
    parser = argparse.ArgumentParser(
        description="Financial Assistant powered by LangGraph agents"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Run in interactive mode"
    )
    parser.add_argument("--eval", "-e", action="store_true", help="Run evaluation mode")

    args = parser.parse_args()

    if args.interactive and args.eval:
        print("Error: Cannot specify both interactive and eval modes")
        sys.exit(1)
    elif args.interactive:
        asyncio.run(main_interactive())
    elif args.eval:
        asyncio.run(main_eval())
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
