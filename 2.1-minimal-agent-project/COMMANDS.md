# Commands for this lesson

Reference for the commands used in this lesson, in the order you run them.

## Setup (run once)

Set your GCP project:

```bash
gcloud config set project YOUR_PROJECT_ID
```

Enable the required APIs:

```bash
gcloud services enable aiplatform.googleapis.com
```

## Prepare the project

After uploading and extracting the zip, open the project in the Cloud Shell Editor:

```bash
cd ~/minimal-agent-project
cloudshell open-workspace ~/minimal-agent-project
```

Copy the environment template to a working `.env` file:

```bash
cp .env.example .env
```

Then edit `.env` and replace `YOUR_PROJECT_ID` with your actual project ID. You can find it with:

```bash
gcloud config get-value project
```

## Install dependencies

From inside the project directory:

```bash
pip install -e . --break-system-packages
```

This reads `pyproject.toml` and installs the pinned versions.

## Run the agent

From the outer project directory (`~/minimal-agent-project`):

```bash
adk web --allow_origins "regex:.*"
```

Then open Cloud Shell's Web Preview on port 8000 to access the dev UI.

Stop the server with Ctrl+C when done.
