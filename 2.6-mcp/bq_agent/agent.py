import os
import google.auth
from google.adk.agents import LlmAgent
from google.adk.agents.readonly_context import ReadonlyContext
from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool.mcp_session_manager import StreamableHTTPConnectionParams
from google.auth.transport.requests import Request
from google.adk.tools.preload_memory_tool import PreloadMemoryTool

from .tools import get_my_gcp_project_info
from .shared_libraries.callbacks import fix_billing_project, truncate_large_responses

# Credentials object lives at module level. The token inside it gets refreshed
# on every MCP request by the header_provider below.
_credentials, _ = google.auth.default(
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)

def mcp_header_provider(context: ReadonlyContext) -> dict[str, str]:
    """Returns fresh auth headers for every MCP request."""
    _credentials.refresh(Request())
    return {
        "Authorization": f"Bearer {_credentials.token}",
        "X-Goog-User-Project": os.environ["GOOGLE_CLOUD_PROJECT"],
    }
    
mcp_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
} 

bigquery_mcp_toolset = McpToolset(
    connection_params=StreamableHTTPConnectionParams(
        url="https://bigquery.googleapis.com/mcp",
        headers=mcp_headers,
    ),
    header_provider=mcp_header_provider,
)

root_agent = LlmAgent(
    model="gemini-3.5-flash",
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
    tools=[get_my_gcp_project_info, bigquery_mcp_toolset, PreloadMemoryTool()],
    before_tool_callback=fix_billing_project,
    after_tool_callback=truncate_large_responses,
)
