import chainlit as cl  # type: ignore
from agents import Agent, OpenAIChatCompletionsModel, RunConfig, Runner , function_tool
from openai import AsyncOpenAI
from openai.types.responses import ResponseTextDeltaEvent

api_key = "AIzaSyDROvIULVM63UyJxjsUiKxHtNqTT_jXoBA"




@cl.on_chat_start
async def on_chat_start():
    external_client = AsyncOpenAI(
        api_key=api_key,
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    model = OpenAIChatCompletionsModel(
        model="gemini-2.0-flash",
        openai_client=external_client
    )
    agent = Agent(
        name="Assistant",
        model=model,
        instructions="You are a helpful assistant."
    )
    cl.user_session.set("agent", agent)
    cl.user_session.set("model", model)
    cl.user_session.set("external_client", external_client)
    cl.user_session.set("history", [])
    await cl.Message(content="Hello! I'm your personal assistant. How can I help you today?").send()


@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("history")
    agent = cl.user_session.get("agent")
    model = cl.user_session.get("model")
    external_client = cl.user_session.get("external_client")

    history.append({"role": "user", "content": message.content})

    run_config = RunConfig(
        model=model,
        model_provider=external_client,
        tracing_disabled=True
    )

    result = Runner.run_streamed(agent, input=history, run_config=run_config)

    msg = cl.Message(content="")  # Start with an empty message
    final_response = ""   

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            delta = event.data.delta or ""
            final_response += delta
            await msg.stream_token(delta)
            print(event.data.delta, end="", flush=True)
            
    await msg.send()

    history.append({"role": "assistant", "content": result.final_output})
    cl.user_session.set("history", history)