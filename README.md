# Basic Agents

A collection of basic AI agent implementations using the `openai-agents` library.

## Projects

### 1. Async Hello Agent
A FastAPI-based chat application with a beautiful glassmorphism UI and a CLI chatbot.

#### How to Run

1. **Setup Environment**:
   Ensure you have a `.env` file in the `async-hello-agent` directory with your `OPENROUTER_API_KEY`.
   ```env
   OPENROUTER_API_KEY=your_key_here
   ```

2. **Install Dependencies**:
   ```bash
   cd async-hello-agent
   uv sync
   ```

3. **Run Terminal Chat**:
   ```bash
   uv run python main.py
   ```

4. **Run Web Interface**:
   ```bash
   uv run uvicorn server:app --port 8000
   ```
   Then open [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

## Tech Stack
- **Backend**: Python, FastAPI, Uvicorn
- **AI**: openai-agents, OpenRouter (open-source models)
- **Frontend**: Vanilla HTML/JS/CSS (Glassmorphism design)

## Project Status
- **Status**: ✅ Fully Functional
- **Last Updated**: May 2026