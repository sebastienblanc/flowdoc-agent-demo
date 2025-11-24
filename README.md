# flowdoc-agent-demo

An automated system for generating comprehensive documentation for GitHub Actions workflows.

## Overview

This repository demonstrates an agentic approach to automatically documenting GitHub Actions workflows. Whenever a workflow file is added or modified, an agent automatically generates detailed markdown documentation.

## How It Works

The system consists of three main components:

### 1. Docker Compose Agent (`compose.agent.yml`)

A Docker Compose configuration that defines the workflow documentation agent. It:
- Uses Python 3.11 in a containerized environment
- Installs necessary dependencies (PyYAML)
- Runs the documentation generation script
- Can be triggered based on workflow file changes

### 2. Documentation Generator Script (`scripts/document_workflows.py`)

A Python script that:
- Scans all workflow files in `.github/workflows/`
- Parses YAML workflow definitions
- Generates comprehensive markdown documentation including:
  - Workflow name and metadata
  - Trigger events (push, pull_request, etc.)
  - Environment variables
  - Job configurations
  - Step-by-step breakdown of each job
  - Matrix build strategies
- Creates an index of all documented workflows

### 3. GitHub Actions Workflow (`.github/workflows/document-workflows.yml`)

A GitHub Actions workflow that:
- Triggers on changes to workflow files
- Executes the Docker Compose agent
- Commits generated documentation back to the repository
- Uploads documentation as workflow artifacts

## Generated Documentation

All generated documentation is stored in the `docs/workflows/` directory:
- Each workflow gets its own `.md` file
- A `README.md` index file lists all documented workflows
- Documentation is automatically updated on every workflow change

## Usage

### Automatic Documentation

Documentation is generated automatically whenever:
1. A workflow file is added or modified in `.github/workflows/`
2. Changes are pushed to the main/master branch
3. A pull request modifies workflow files
4. The workflow is manually triggered via `workflow_dispatch`

### Manual Documentation Generation

You can also generate documentation manually using Docker Compose:

```bash
docker-compose -f compose.agent.yml --profile agent run --rm workflow-documenter
```

Or directly with Python:

```bash
pip install pyyaml
python scripts/document_workflows.py
```

## Example

See the automatically generated documentation:
- [All Workflows](docs/workflows/README.md)
- [Document Workflows](docs/workflows/document-workflows.md)
- [Example CI Workflow](docs/workflows/example-ci.md)

## Benefits

- **Always Up-to-Date**: Documentation is regenerated on every workflow change
- **Comprehensive**: Captures all workflow details automatically
- **Consistent**: Uses a standardized format for all workflows
- **Low Maintenance**: No manual documentation updates required
- **Self-Documenting**: The system documents its own workflow!

## Requirements

- Docker and Docker Compose
- GitHub Actions enabled on the repository
- Write permissions for GitHub Actions (to commit documentation)

## License

This is a demonstration repository for educational purposes.