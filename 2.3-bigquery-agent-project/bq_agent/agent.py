from google.adk.agents import LlmAgent
from .tools import get_my_gcp_project_info

import google.auth
from google.adk.tools.bigquery import BigQueryCredentialsConfig, BigQueryToolset
from google.adk.tools.bigquery.config import BigQueryToolConfig, WriteMode

credentials, _ = google.auth.default()
credentials_config = BigQueryCredentialsConfig(credentials=credentials)
tool_config = BigQueryToolConfig(write_mode=WriteMode.BLOCKED)

bigquery_toolset = BigQueryToolset(
    credentials_config=credentials_config, bigquery_tool_config=tool_config
)

root_agent = LlmAgent(
    model="gemini-3.5-flash",
    name="bq_agent",
    tools=[get_my_gcp_project_info, bigquery_toolset],
    instruction=(
        "You are a helpful assistant with access to information about the user's "
        "GCP project and access to BigQuery. You can answer questions about the "
        "user's project, query BigQuery datasets they have access to, and explore "
        "public datasets like bigquery-public-data.stackoverflow. When the user "
        "asks a question that requires data, use BigQuery to find the answer."
    ),
)
