# Async Hello Agent

This is a basic AI agent implementation using `openai-agents` and OpenRouter.

## Features
- **CLI Chatbot**: Interactive terminal-based chat.
- **Web Interface**: Modern, responsive UI with streaming support.
- **Async Execution**: Built with `asyncio` and `FastAPI`.

## Installation

```bash
uv sync
```

## Usage

### CLI
```bash
uv run python main.py
```

### Web
```bash
uv run uvicorn server:app --port 8000
```
Visit `http://127.0.0.1:8000`
