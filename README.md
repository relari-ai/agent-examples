# Example Multi-Agent Application built using different agent orchestration frameworks

This repository showcases an example multi-agent application built using different agent orchestration framework, currently it includes:
* [LangGraph](https://github.com/langchain-ai/langgraph)
* [CrewAI](https://github.com/crewAIInc/crewAI)
* [OpenAI Swarm](https://github.com/openai/swarm)


It's designed as an educational reference for developers to understand the differences and capabilities of each agent orchestration framework.

**Check out our detailed write-up: [Choosing the Right AI Agent Framework: LangGraph vs CrewAI vs OpenAI Swarm](https://www.relari.ai/blog/ai-agent-framework-comparison-langgraph-crewai-openai-swarm#introduction)**

## Agentic Finance Assistant implemented using LangGraph, CrewAI and OpenAI Swarm

A finance-focused agent built using the LangGraph, CrewAI and OpenAI Swarm agent orchestration frameworks. This agent can handle financial queries, fetch real-time stock data, research through the internet,and provide comprehensive financial reports. 

Note that the finance agents requires a free API key from the [FMP API](https://site.financialmodelingprep.com/developer/docs) to fetch financial data.

**Agentic Finance Assistant Architecture:**

![Agent Architecture](https://cdn.prod.website-files.com/669f7329c898141d69e166b3/674511356e6f4daeb00041eb_6745111cd46789116c371f5c_agentic-finance-assistant-relari.png)


**Installation:**

```bash
cd apps/langgraph-fin-agent # or crewai-fin-agent or swarm-fin-agent
poetry install
```

Create a `.env` file and add your OpenAI API key and FMP API key.

**Run:**

```bash
poetry run python src/main.py
```

## Verification with Agent Contracts

[Agent Contracts](https://github.com/relari-ai/agent-contracts) is a tool developed by Relari to define, verify and certify agentic AI systems.

The langgraph-fin-agent example includes instrumentation to run verification using a pre-defined specification. Checkout the [README of langgraph-fin-agent](apps/langgraph-fin-agent/README.md) for more details.