import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if openrouter_api_key:
    openrouter_api_key = openrouter_api_key.strip("\"'")

if not openrouter_api_key:
    raise ValueError("Error: OPENROUTER_API_KEY not found in .env file.")

external_client = AsyncOpenAI(
    api_key=openrouter_api_key,
    base_url="https://openrouter.ai/api/v1",
)

model = OpenAIChatCompletionsModel(
    model="openrouter/free",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

agent = Agent(
    name="Assistant",
    instructions="You are helpful Assistant.",
    model=model
)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

from fastapi.responses import StreamingResponse

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    async def text_generator():
        try:
            # OpenRouter recommends these headers
            extra_headers = {
                "HTTP-Referer": "https://github.com/syedahsanrazabukhari/basic-agents",
                "X-Title": "Basic Agents Chatbot",
            }
            
            # Using the agent's instructions as the system message
            stream = await external_client.chat.completions.create(
                model=model.model,
                messages=[
                    {"role": "system", "content": agent.instructions},
                    {"role": "user", "content": request.message}
                ],
                stream=True,
                extra_headers=extra_headers
            )
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            error_msg = str(e)
            print(f"Error in chat_endpoint: {error_msg}")
            if "401" in error_msg or "api_key" in error_msg.lower():
                yield "\n\n[Error: API Key invalid or not found. Please check your .env file.]"
            else:
                yield f"\n\n[Error: {error_msg}]"

    return StreamingResponse(text_generator(), media_type="text/plain")

# Ensure static folder exists
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")
