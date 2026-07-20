import os

import vertexai

from vertexai import agent_engines

from bq_agent.agent import root_agent

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
PROJECT_LOCATION = "us-central1"
STAGING_BUCKET = f"gs://{PROJECT_ID}-staging"
RESOURCE_NAME = os.environ["AGENT_RESOURCE_NAME"]

client = vertexai.Client(project=PROJECT_ID, location=PROJECT_LOCATION)
app = agent_engines.AdkApp(agent=root_agent, enable_tracing=True)

remote_agent = client.agent_engines.update(
    name=RESOURCE_NAME,
    agent=app,
    config={
        "staging_bucket": STAGING_BUCKET,
        "display_name": "bq-agent",
        "description": "BigQuery MCP agent",
        "requirements": [
            "google-adk==1.33.0",
            "google-cloud-aiplatform==1.153.1",
            "google-cloud-resource-manager==1.14.0",
            "mcp==1.27.0",
            "pydantic>=2.12.5",
            "cloudpickle>=3.1.2",
        ],
        "extra_packages": ["./bq_agent"],
    },
)
print(f"\nDeployed agent resource name:\n{remote_agent.api_resource.name}")