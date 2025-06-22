import asyncio
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig

gemini_api_key = "AIzaSyDyPk2jh64uJ_kzgPKvxcdB-lOqhvjKymU"

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set")


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

async def main():
    
    agent: Agent = Agent(name="Problem-Solver", instructions="You are a problem solver who is able to solve problems.", model=model)

    result = await Runner.run(agent, "I have a problem with my computer. Please help me solve it.", run_config=config)

    print(result)

asyncio.run(main())


# run, run_sync, run_streamed

# run_sync is used to run the agent in a synchronous manner.

# run_streamed is used to run the agent in a streamed manner.

# run is used to run the agent in an asynchronous manner.
