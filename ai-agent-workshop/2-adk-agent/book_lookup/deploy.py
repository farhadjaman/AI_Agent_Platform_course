import os
import vertexai
from dotenv import dotenv_values
from vertexai.agent_engines import AdkApp

# If running from within the book_lookup directory, import agent directly
from agent import root_agent

# --- Configuration ---
PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "autoreels-467111")
LOCATION = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
STAGING_BUCKET = f"gs://{PROJECT_ID}-agent-staging"

# --- Create the app and client ---

# Initialize Vertex AI with project and location
vertexai.init(project=PROJECT_ID, location=LOCATION, staging_bucket=STAGING_BUCKET)

app = AdkApp(agent=root_agent)
client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

# Prepare environment variables
env_vars = {
    "GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY": "true",
    "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT": "true",
}

# Load variables from .env file if it exists and merge them
# if os.path.exists(".env"):
#     print("Loading environment variables from .env...")
#     env_vars.update(dotenv_values(".env"))

print(f"Deploying agent to Reasoning Engine in project: {PROJECT_ID}...")
print("This usually takes 3-5 minutes.\n")

remote_agent = client.agent_engines.create(
    agent=app,
    config={
        "display_name": "book-lookup-agent",
        "requirements": [
            "google-cloud-aiplatform[reasoningengine,adk]",
            "google-adk",
            "requests",
            "cloudpickle",
            "pydantic",
            "python-dotenv",
        ],
        "staging_bucket": STAGING_BUCKET,
        "extra_packages": ["."], # Bundles the current 'book_lookup' directory
        "env_vars": env_vars,
    },
)