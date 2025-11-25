# Document Workflows

## Metadata

- **Workflow File Name:** document-workflows.yml  
- **Last Generated Timestamp:** YYYY-MM-DD HH:mm:ss UTC

## Triggers

This GitHub Actions workflow is triggered by:
- a `push` event on the branches `main` and `master`, specifically for paths containing `.github/workflows/*.yml` or `.github/workflows/*.yaml`.
- a `pull_request` event on paths containing `.github/workflows/*.yml` or `.github/workflows/*.yaml`.
- a manual workflow dispatch.

## Environment Variables

The workflow does not use any environment variables defined at the workflow level.

## Jobs

This workflow contains three jobs:

### Job: Document Workflow

#### Steps

1. **Checkout repository**
    - Uses action `actions/checkout@v4`  
    - Checks out the repository with a shallow clone using `fetch-depth: 0` to reduce cloning time.

2. **Set up Docker Compose**

    - Runs a command to check the version of Docker Compose.
    
3. **Run documentation agent**
    - Uses a custom script to run a Docker service named `agent`. The script specifies a profile (`agent`) and runs `workflow-documenter` as a one-off container.

4. **Check for documentation changes**
    - Initializes an output variable `has_changes`.
    - Executes a Git diff to check if any files have changed in the repository's `docs/workflows/` directory.
    - Sets the `has_changes` variable to either `true` or `false` and prints a message indicating whether documentation changes are detected.

5. **Commit documentation (if needed)**
    - Conditional step based on the output of the `check_changes` step.
    - Configures global Git user information and adds all files in `docs/workflows/`.
    - Creates a new commit to push changes upstream.
    
6. **Upload documentation as artifact (if needed)**
    - Another conditional step based on the output of the `check_changes` step.
    - Uses the GitHub Actions `upload-artifact@v4` action to upload `docs/workflows/` as an artifact named `workflow-docs`.
    - Specifies a retention period of 30 days for the artifact.

### Other Jobs

This workflow does not contain any additional jobs under the main job description, but you can include more complex logic by adding more actions and steps as needed.