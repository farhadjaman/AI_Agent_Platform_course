# 2-adk-agent/request_to_agent_engine.py

import asyncio
import os
import vertexai

# --- Configuration ---

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "gcpstudyhub-ai-agents-1")
LOCATION = "us-central1"
RESOURCE_NAME = "projects/480960590623/locations/us-central1/reasoningEngines/688301425813356544"  # paste the resource name returned by deploy.py


# --- Connect to the deployed agent ---

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
remote_agent = client.agent_engines.get(name=RESOURCE_NAME)


# --- Helper to print clean output ---

def print_event(event):
    content = event.get("content", {})
    parts = content.get("parts", [])
    for part in parts:
        if "function_call" in part:
            fc = part["function_call"]
            print(f"  [Tool call] {fc['name']}({fc['args']})")
        elif "function_response" in part:
            fr = part["function_response"]
            print(f"  [Tool result] {fr['name']} returned: {fr['response']}")
        elif "text" in part:
            print(f"  [Agent] {part['text']}")


# --- Interactive chat with session persistence ---

async def main():
    session = await remote_agent.async_create_session(user_id="test-user")
    session_id = session["id"]
    print(f"Session created: {session_id}")
    print("Type your questions below. Press Ctrl+C to exit.\n")

    while True:
        try:
            user_input = input("You: ")
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if not user_input.strip():
            continue

        async for event in remote_agent.async_stream_query(
            user_id="test-user",
            session_id=session_id,
            message=user_input,
        ):
            print_event(event)

        print()


if __name__ == "__main__":
    asyncio.run(main())