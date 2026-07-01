from google.adk.agents import LlmAgent
from google.adk.tools.bigquery import BigQueryToolset

from .tools import get_my_gcp_project_info


bigquery_toolset = BigQueryToolset()


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
    tools=[get_my_gcp_project_info, bigquery_toolset],
)
