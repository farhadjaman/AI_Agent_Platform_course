import os
import vertexai
PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
RESOURCE_NAME = "projects/480960590623/locations/us-central1/reasoningEngines/3285726122620223488"
client = vertexai.Client(project=PROJECT_ID, location=LOCATION)
remote_agent = client.agent_engines.get(name=RESOURCE_NAME)
session = remote_agent.create_session(user_id="smoke-test-user")
print(f"Session created: {session['id']}\n")
query = "What's my GCP project ID, and how many rows are in bigquery-public-data.stackoverflow.posts_questions?"
print(f"Q: {query}\n")
print("A: ", end="", flush=True)
for event in remote_agent.stream_query(
    user_id="smoke-test-user",
    session_id=session["id"],
    message=query,
):
    if "content" in event:
        parts = event["content"].get("parts", [])
        for part in parts:
            if "text" in part:
                print(part["text"], end="", flush=True)
print("\n")