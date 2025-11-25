# flowdoc-agent-demo

An automated system for generating comprehensive documentation for GitHub Actions workflows using Docker's AI features.

## Overview

This repository demonstrates an agentic approach to automatically documenting GitHub Actions workflows using Docker Compose AI models. Whenever a workflow file is added or modified, an AI agent automatically analyzes and generates detailed markdown documentation.

## How It Works

The system consists of three main components:

### 1. Docker Compose Agent (`compose.agent.yml`)

A Docker Compose configuration that uses Ollama for local AI model execution:
- Sets up Ollama service to run AI models locally
- Downloads and configures Qwen 2.5 Coder model for documentation generation
- Configures a `workflow-documenter` service with AI-powered analysis
- Uses environment variables to provide system instructions and prompts to the AI
- Can be triggered based on workflow file changes

### 2. AI Documentation Service (`ai.documenter/`)

A Go-based service using Firebase Genkit that:
- Connects to Docker's AI model runner
- Reads GitHub Actions workflow YAML files
- Uses AI to analyze and understand workflow configurations
- Generates comprehensive, natural-language markdown documentation
- Creates an index of all documented workflows

The AI is instructed to analyze:
- Workflow names and metadata
- Trigger events (push, pull_request, etc.)
- Environment variables
- Job configurations and dependencies
- Step-by-step breakdown of each job
- Matrix build strategies

### 3. GitHub Actions Workflow (`.github/workflows/document-workflows.yml`)

A GitHub Actions workflow that:
- Triggers on changes to workflow files
- Executes the Docker Compose AI agent
- Commits AI-generated documentation back to the repository
- Uploads documentation as workflow artifacts

## Generated Documentation

All generated documentation is stored in the `docs/workflows/` directory:
- Each workflow gets its own AI-generated `.md` file
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
docker compose -f compose.agent.yml --profile agent run --rm workflow-documenter
```

## Example

See the automatically generated documentation:
- [All Workflows](docs/workflows/README.md)
- [Document Workflows](docs/workflows/document-workflows.md)
- [Example CI Workflow](docs/workflows/example-ci.md)

## Benefits

- **AI-Powered**: Uses large language models to generate natural, comprehensive documentation
- **Always Up-to-Date**: Documentation is regenerated on every workflow change
- **Intelligent Analysis**: AI understands context and explains complex workflow patterns
- **Consistent**: Uses AI prompts to ensure standardized documentation format
- **Low Maintenance**: No manual documentation updates required
- **Self-Documenting**: The system documents its own workflow!

## Requirements

- Docker and Docker Compose
- GitHub Actions enabled on the repository
- Write permissions for GitHub Actions (to commit documentation)

## Technical Details

This implementation uses:
- **Ollama**: Local AI model runner for executing language models
- **Firebase Genkit**: Go framework for building AI-powered applications
- **OpenAI-compatible API**: Ollama provides OpenAI-compatible endpoints
- **Qwen 2.5 Coder**: Specialized coding model optimized for understanding code and technical documentation

## License

This is a demonstration repository for educational purposes.