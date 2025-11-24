# Document Workflows
**Workflow File:** `document-workflows.yml`
**Last Generated:** 2025-11-24 21:39:47 UTC
---
## Triggers

### push
- **branches:**
  - `main`
  - `master`
- **paths:**
  - `.github/workflows/*.yml`
  - `.github/workflows/*.yaml`

### pull_request
- **paths:**
  - `.github/workflows/*.yml`
  - `.github/workflows/*.yaml`

### workflow_dispatch
- Event triggered without additional configuration

## Jobs

### document
**Name:** Generate Workflow Documentation

**Runs on:** `ubuntu-latest`

**Steps:**

1. **Checkout repository**
   - Uses: `actions/checkout@v4`
   - With:
     - fetch-depth: `0`

2. **Set up Docker Compose**
   - Run:
     ```
     docker compose version
     ```

3. **Run documentation agent**
   - Run:
     ```
     docker compose -f compose.agent.yml --profile agent run --rm workflow-documenter
     ```

4. **Check for documentation changes**
   - Run: Multi-line command (8 lines)
     ```
     git add docs/workflows/
     if git diff --staged --quiet; then
     echo "has_changes=false" >> $GITHUB_OUTPUT
     ...
     ```

5. **Commit documentation**
   - Run: Multi-line command (5 lines)
     ```
     git config --global user.name 'github-actions[bot]'
     git config --global user.email 'github-actions[bot]@users.noreply.github.com'
     git add docs/workflows/
     ...
     ```

6. **Upload documentation as artifact**
   - Uses: `actions/upload-artifact@v4`
   - With:
     - name: `workflow-docs`
     - path: `docs/workflows/`
     - retention-days: `30`

