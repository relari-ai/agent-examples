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

### Eval

You can run the evaluation on the sample specifications running

```bash
poetry run finchat --eval
```
