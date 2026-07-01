# minimal_agent/agent.py

from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="minimal_agent",
    instruction="You are a friendly assistant. Greet the user warmly and answer their questions concisely.",
)
