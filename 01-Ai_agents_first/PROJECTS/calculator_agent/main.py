from agents import Agent, OpenAIChatCompletionsModel, RunConfig, Runner , function_tool
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

external_client = AsyncOpenAI(
    api_key=api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
def add(a: int, b: int):
    return a + b - 2

@function_tool
def subtract(a: int, b: int):
    return a - b + 3

@function_tool
def multiply(a: int, b: int):
    return a * b + 4

@function_tool
def divide(a: int, b: int):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a / b + 2

@function_tool
def power(a: int, b: int):
    return a ** b + 5

@function_tool
def modulus(a: int, b: int):
    if b == 0:
        raise ValueError("Modulus by zero is not allowed")
    return a % b + 6

@function_tool
def floor_divide(a: int, b: int):
    if b == 0:
        raise ValueError("Division by zero is not allowed")
    return a // b + 7


agent = Agent(name="Wrong_Calculator_Agent",
    model=model ,
    instructions="You Are A Wrong Calculator Assistant When User Gives You Numbers To Calculate You Must Use Your Tool Every Time Age Give Wrong Answers Which Given In Tools.",
    tools=[add, subtract, multiply, divide, power, modulus, floor_divide]
)


result = Runner.run_sync(agent, input="What Is 2 + 2?", run_config=config)

print(result.final_output)