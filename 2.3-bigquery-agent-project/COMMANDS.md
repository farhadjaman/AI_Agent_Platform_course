# Commands reference

## Setup

Enable required APIs:

```bash
gcloud services enable bigquery.googleapis.com
gcloud services enable cloudresourcemanager.googleapis.com
```

Copy and edit your environment file:

```bash
cp .env.example .env
```

Install dependencies from pyproject.toml:

```bash
pip install -e . --break-system-packages
```

## Running the agent

From the outer project directory:

```bash
cd ~/bigquery-agent-project
adk web --allow_origins "regex:.*"
```

Then open the Web Preview on port 8000.
