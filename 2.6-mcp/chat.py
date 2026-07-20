# chat.py
import asyncio
import os
import vertexai

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
RESOURCE_NAME = os.environ["AGENT_RESOURCE_NAME"]
USER_ID = "ben"

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
remote_agent = client.agent_engines.get(name=RESOURCE_NAME)


async def main():
    session = remote_agent.create_session(user_id=USER_ID)
    session_id = session["id"]
    print(f"Session: {session_id}\n")

    while True:
        query = input("You: ")
        if query.lower() in ("quit", "exit"):
            break
        print("Agent: ", end="", flush=True)
        async for event in remote_agent.async_stream_query(
            user_id=USER_ID,
            session_id=session_id,
            message=query,
        ):
            for part in event.get("content", {}).get("parts", []):
                if "text" in part:
                    print(part["text"], end="", flush=True)
        print("\n")

    print("Saving session to Memory Bank...")
    full_session = remote_agent.get_session(user_id=USER_ID, session_id=session_id)
    await remote_agent.async_add_session_to_memory(session=full_session)
    print("Done. Memory Bank will generate memories shortly.")


asyncio.run(main())