from google.adk.agents import LlmAgent

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="alphabet_analyst",
    instruction="You are a friendly assistant. Greet the user warmly and answer their questions concisely.",
)
