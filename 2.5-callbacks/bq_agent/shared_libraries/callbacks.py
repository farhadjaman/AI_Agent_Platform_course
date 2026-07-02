import os
from typing import Any
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext

MAX_ROWS_IN_CONTEXT = 50

def fix_billing_project(tool:BaseTool, args: dict[str, Any], tool_context: ToolContext):
    """Rewrites bigquery-public-data billing project to the user's own project."""
    if tool.name != "execute_sql":
        return None

    if args.get("project_id") == "bigquery-public-data":
        args["project_id"] = os.environ["GOOGLE_CLOUD_PROJECT"]

    return None

def truncate_large_responses(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict
):
    """Truncates BigQuery results that would blow out the context window."""

    if tool.name != "execute_sql":
        return None

    rows = tool_response.get("rows")
    if rows is None or len(rows) <= MAX_ROWS_IN_CONTEXT:
        return None


    truncated = {
        **tool_response,
        "rows": rows[:MAX_ROWS_IN_CONTEXT],
        "note": f"Result truncated from {len(rows)} rows to {MAX_ROWS_IN_CONTEXT} by callback.",
    }
    return truncated