# Commands reference

## Setup

Enable MCP for BigQuery:

```bash
gcloud beta services mcp enable bigquery.googleapis.com
```

Grant your account the MCP tool user role:

```bash
USER_EMAIL=$(gcloud config get-value account)
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member="user:$USER_EMAIL" \
  --role="roles/mcp.toolUser"
```

Copy and edit your environment file:

```bash
cp .env.example .env
```

## Add the mcp dependency

Open pyproject.toml and add this line to the dependencies list:

```
"mcp==1.27.0",
```

Then install:

```bash
pip install . --break-system-packages
```

## The swap

Edit bq_agent/agent.py per the lesson. The final file should look like:

```python
# bq_agent/agent.py

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
```

## Update the callbacks

Replace the contents of bq_agent/shared_libraries/callbacks.py with:

```python
"""Callback functions for bq_agent."""

import os
from typing import Any
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext


MAX_ROWS_IN_CONTEXT = 50

# Tool names from the BigQuery MCP server. execute_sql_readonly is restricted
# to SELECT; execute_sql can also run writes. We handle both so the callback
# fires whichever the model picks.
BIGQUERY_QUERY_TOOLS = ("execute_sql", "execute_sql_readonly")


def fix_billing_project(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
):
    """Forces billing project to the user's own project for all BigQuery query calls.

    This is a guardrail. The model can pass arbitrary project IDs in BigQuery
    queries: it might invent a placeholder, reference bigquery-public-data
    (where it can read but can't bill), or pull a project name from earlier in
    the conversation. We don't want the agent deciding which project to bill.
    The callback pins billing to the user's own project, every time.
    """
    if tool.name not in BIGQUERY_QUERY_TOOLS:
        return None

    project_key = "projectId" if "projectId" in args else "project_id"
    args[project_key] = os.environ["GOOGLE_CLOUD_PROJECT"]

    return None


def truncate_large_responses(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict
):
    """Truncates BigQuery results that would blow out the context window.

    MCP responses wrap data inside structuredContent, so we navigate there
    instead of looking at the top level.
    """
    if tool.name not in BIGQUERY_QUERY_TOOLS:
        return None

    structured = tool_response.get("structuredContent", {})
    rows = structured.get("rows")
    if rows is None or len(rows) <= MAX_ROWS_IN_CONTEXT:
        return None

    truncated_structured = {
        **structured,
        "rows": rows[:MAX_ROWS_IN_CONTEXT],
        "note": f"Result truncated from {len(rows)} rows to {MAX_ROWS_IN_CONTEXT} by callback.",
    }
    return {**tool_response, "structuredContent": truncated_structured}
```

## Running the agent

From the outer project directory:

```bash
cd ~/bigquery-agent-mcp
adk web --allow_origins "regex:.*"
```

Then open the Web Preview on port 8000. Pick bq_agent from the dropdown. Ignore the build/ and egg-info entries.

## Test question

```
What are the top 5 most-viewed Python questions on Stack Overflow ever?
```
