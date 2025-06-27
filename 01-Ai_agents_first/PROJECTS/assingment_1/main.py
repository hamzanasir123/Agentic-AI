from agents import Agent, InputGuardrail, GuardrailFunctionOutput, InputGuardrailTripwireTriggered, Runner
from pydantic import BaseModel
import asyncio
from config import config


# Output model
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# Agents (remove the `openai_api_key` argument)
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples.",
)

history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

# Guardrail
async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context, run_config=config)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )

# Triage agent
triage_agent = Agent(
    name="Triage Agent",
    instructions="You determine which agent to use based on the user's homework question.",
    handoffs=[history_tutor_agent, math_tutor_agent],
    input_guardrails=[
        InputGuardrail(guardrail_function=homework_guardrail),
    ],
)

# Main function
async def main():
    try:
        result1 = await Runner.run(triage_agent, "who was the first president of the united states?", run_config=config)
        print("Output 1:", result1.final_output)
    except Exception as e:
        print("Error in query 1:", str(e))

    try:
        result2 = await Runner.run(triage_agent, "what is life", run_config=config)
        print("Output 2:", result2.final_output)
    except InputGuardrailTripwireTriggered as e:
        reasoning = e.result.function_output.output_info.reasoning
        print("Output 2 was blocked by guardrail:")
        print("→", reasoning)

# Run the async main
if __name__ == "__main__":
    asyncio.run(main())
