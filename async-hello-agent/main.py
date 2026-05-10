import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio

load_dotenv()

openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
if openrouter_api_key:
    openrouter_api_key = openrouter_api_key.strip("\"'")

if not openrouter_api_key:
    raise ValueError("Error: OPENROUTER_API_KEY not found in .env file. Add your OpenRouter API key to proceed.")

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


async def main():
    agent = Agent(
        name="Assistant",
        instructions="You are helpful Assistent.",
        model=model
    )

    print("Chatbot started! Type 'exit' to stop the conversation.\n")
    while True:
        user_input = input("whats your Question: ")
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Conversation ended. Goodbye!")
            break
            
        result = await Runner.run(agent, user_input, run_config=config)
        print(f"\nAssistant: {result.final_output}\n")



if __name__ == "__main__":
    asyncio.run(main())