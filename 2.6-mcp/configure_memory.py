# configure_memory.py
import os
import vertexai
from vertexai._genai.types.common import (
    ReasoningEngineContextSpec,
    ReasoningEngineContextSpecMemoryBankConfig,
    MemoryBankCustomizationConfig,
    MemoryBankCustomizationConfigMemoryTopic,
    MemoryBankCustomizationConfigMemoryTopicCustomMemoryTopic,
)

PROJECT_ID = os.environ["GOOGLE_CLOUD_PROJECT"]
LOCATION = "us-central1"
RESOURCE_NAME = os.environ["AGENT_RESOURCE_NAME"]

client = vertexai.Client(project=PROJECT_ID, location=LOCATION)

context_spec = ReasoningEngineContextSpec(
    memory_bank_config=ReasoningEngineContextSpecMemoryBankConfig(
        customization_configs=[
            MemoryBankCustomizationConfig(
                memory_topics=[
                    MemoryBankCustomizationConfigMemoryTopic(
                        custom_memory_topic=MemoryBankCustomizationConfigMemoryTopicCustomMemoryTopic(
                            label="gcp_and_bigquery_preferences",
                            description=(
                                "The user's preferences around GCP services, BigQuery datasets, "
                                "programming languages, and data engineering workflows. "
                                "Examples: preferred query languages, favorite public datasets, "
                                "current project focus, tools they like to use."
                            ),
                        )
                    )
                ]
            )
        ]
    )
)

result = client.agent_engines.update(
    name=RESOURCE_NAME,
    config={"context_spec": context_spec},
)
print(f"Updated. update_time: {result.api_resource.update_time}")