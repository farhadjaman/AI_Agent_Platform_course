# Commands reference

## Setup

Enable required APIs:

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable vectorsearch.googleapis.com
```

Install dependencies from pyproject.toml:

```bash
pip install . --break-system-packages
```

Copy and edit your environment file with your project ID and corpus ID:

```bash
cp .env.example .env
```

## Running the agent

From the project directory, source the env vars and start adk web:

```bash
cd ~/alphabet-analyst-project
set -a; source .env; set +a
adk web --allow_origins "regex:.*"
```

Then open the Web Preview on port 8000 and select `alphabet_analyst` from the dropdown.
