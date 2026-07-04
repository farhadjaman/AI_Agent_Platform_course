import google.auth

from google.adk.agents import LlmAgent
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.auth.transport.requests import Request

from .tools import get_my_gcp_project_info
from .shared_libraries.callbacks import fix_billing_project, truncate_large_responses


def get_auth_headers() -> dict[str, str]:
    """Fetch auth headers for the managed MCP endpoint."""
    credentials, _ = google.auth.default(
        scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )
    credentials.refresh(Request())
    return {"Authorization": f"Bearer {credentials.token}"}


mcp_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
} | get_auth_headers()

bigquery_mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://bigquery.googleapis.com/mcp",
        headers=mcp_headers,
    )
)

root_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="bq_agent",
    instruction=(
        "You are a helpful assistant with access to information about the user's "
        "GCP project and access to BigQuery. You can answer questions about the "
        "user's project, query BigQuery datasets they have access to, and explore "
        "public datasets like bigquery-public-data.stackoverflow. When the user "
        "asks a question that requires data, use BigQuery to find the answer. "
        "Keep in mind that the bigquery-public-data project is not actually the "
        "project you would run the query in, even though it is the project where "
        "the data resides."
    ),
    tools=[get_my_gcp_project_info, bigquery_mcp_toolset],
    before_tool_callback=fix_billing_project,
    after_tool_callback=truncate_large_responses,
)
