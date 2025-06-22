import chainlit as cl
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

agent: Agent = Agent(name="Personal Assistant", instructions="You are a personal assistant who is able to help with tasks and questions.", model=model)

@cl.on_chat_start
async def start_chat():
    cl.user_session.set("History", [])
    await cl.Message(content="Hello! I'm your personal assistant. How can I help you today?").send()


@cl.on_message
async def handle_message(message: cl.Message):
    history = cl.user_session.get("History")

    history.append({"role": "user", "content": message.content})

    result = await Runner.run(agent, input=history, run_config=config)

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("History", history)

    await cl.Message(content=result.final_output).send()
