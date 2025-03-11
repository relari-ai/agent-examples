# Fin-Chat example (LangGraph)

## Installation

```bash
poetry install
```

Create a file `.env` with

```bash
OPENAI_API_KEY="...."
FMP_API_KEY="...."
```

Where FMP_API_KEY is the API obtained from [FMP API](https://site.financialmodelingprep.com/developer/docs).

## Quickstart

The finchat has two modes `interactive` and `eval`

### Interactive

In interactive mode you can ask your questions in a chat-like fashion.

```bash
poetry run finchat --interactive
```

Each question will create a new trace with the same run-id.

### Run Verification with Agent Contracts

You can run the pre-defined questions in `specifications.json` with the following command.

```bash
poetry run finchat --eval
```

If you want to run verification using [agent-contracts](https://github.com/relari-ai/agent-contracts), please follow the documentation here: [Agent Contracts - Finance Agent Example](https://agent-contracts.relari.ai/examples/finance-agent).