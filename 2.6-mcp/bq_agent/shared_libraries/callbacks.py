# bq_agent/shared_libraries/callbacks.py

"""Callback functions for bq_agent."""

import os
from typing import Any
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext


MAX_ROWS_IN_CONTEXT = 50
BIQQUERY_QUERY_TOOLS = ["execute_sql", "execute_sql_readonly"]


def fix_billing_project(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
):
    """Rewrites bigquery-public-data billing project to user's own project."""
    if tool.name not in BIQQUERY_QUERY_TOOLS:
        return None

    project_key = "projectId" if "projectId" in args else "project_id"

    if args.get(project_key) == "bigquery-public-data":
        args[project_key] = os.environ["GOOGLE_CLOUD_PROJECT"]

    return None


def truncate_large_responses(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext, tool_response: dict
):
    """Truncates BigQuery results that would blow out the context window."""

    if tool.name not in BIQQUERY_QUERY_TOOLS:
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
    return truncated_structured
