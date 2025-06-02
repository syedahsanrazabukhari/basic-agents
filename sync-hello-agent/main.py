import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

if not gemini_api_key:
    raise ValueError("Error: GEMINI_API_KEY not found in .env file. Add your Gemini API key to proceed.")

external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)


agent: Agent = Agent(name="Assistant", instructions="You are a helpful assistant", model=model)

result = Runner.run_sync(agent, "Hello, how are you.", run_config=config)

print("\nCALLING AGENT\n")
print(result.final_output)