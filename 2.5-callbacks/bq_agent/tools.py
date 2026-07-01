"""Custom function tools for bq_agent."""

import os
from google.cloud import resourcemanager_v3


def get_my_gcp_project_info() -> dict:
    """Returns information about the user's current GCP project.

    Use this when the user asks about their project, their project ID,
    their project name, when their project was created, or any other
    metadata about the GCP project they're working in.

    Returns:
        dict: project_id, display_name, state, create_time, and parent.
    """
    project_id = os.environ["GOOGLE_CLOUD_PROJECT"]

    client = resourcemanager_v3.ProjectsClient()
    project = client.get_project(name=f"projects/{project_id}")

    return {
        "project_id": project_id,
        "display_name": project.display_name,
        "state": project.state.name,
        "create_time": project.create_time.isoformat(),
        "parent": project.parent,
    }
