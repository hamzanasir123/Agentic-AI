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

agent: Agent = Agent(name="Doctor", instructions="You are a doctor who is able to diagnose and treat patients.", model=model)

result = Runner.run_sync(agent, "I Have a Fever Plz Suggest Me Some Medicine.", run_config=config)

print("\nCALLING AGENT\n")
print(result.final_output)