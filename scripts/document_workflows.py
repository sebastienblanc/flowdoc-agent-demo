#!/usr/bin/env python3
"""
Workflow Documentation Generator

This script automatically generates markdown documentation for GitHub Action workflows.
It scans the .github/workflows directory and creates detailed documentation for each workflow.
"""

import os
import yaml
import sys
from pathlib import Path
from datetime import datetime, timezone


def load_workflow(workflow_path):
    """Load and parse a GitHub Actions workflow YAML file."""
    try:
        with open(workflow_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {workflow_path}: {e}")
        return None


def generate_workflow_documentation(workflow_path, workflow_data):
    """Generate markdown documentation for a workflow."""
    workflow_name = workflow_data.get('name', os.path.basename(workflow_path))
    
    # Start building the documentation
    doc = []
    doc.append(f"# {workflow_name}\n")
    doc.append(f"**Workflow File:** `{os.path.basename(workflow_path)}`\n")
    doc.append(f"**Last Generated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n")
    doc.append("---\n")
    
    # Description (if available from workflow)
    if 'run-name' in workflow_data:
        doc.append(f"## Description\n\n{workflow_data['run-name']}\n")
    
    # Triggers
    doc.append("## Triggers\n")
    # YAML parses 'on' as True boolean, so check for both
    triggers_key = 'on' if 'on' in workflow_data else True
    if triggers_key in workflow_data:
        triggers = workflow_data[triggers_key]
        if isinstance(triggers, str):
            doc.append(f"- **{triggers}**\n")
        elif isinstance(triggers, list):
            for trigger in triggers:
                doc.append(f"- **{trigger}**\n")
        elif isinstance(triggers, dict):
            for trigger_name, trigger_config in triggers.items():
                doc.append(f"\n### {trigger_name}\n")
                if trigger_config is None:
                    doc.append("- Event triggered without additional configuration\n")
                elif isinstance(trigger_config, dict):
                    for key, value in trigger_config.items():
                        if isinstance(value, list):
                            doc.append(f"- **{key}:**\n")
                            for item in value:
                                doc.append(f"  - `{item}`\n")
                        else:
                            doc.append(f"- **{key}:** `{value}`\n")
                else:
                    doc.append(f"- Triggered on `{trigger_name}` event\n")
    else:
        doc.append("- No triggers defined\n")
    
    # Environment Variables
    if 'env' in workflow_data:
        doc.append("\n## Environment Variables\n")
        for env_name, env_value in workflow_data['env'].items():
            doc.append(f"- **{env_name}:** `{env_value}`\n")
    
    # Jobs
    if 'jobs' in workflow_data:
        doc.append("\n## Jobs\n")
        for job_name, job_config in workflow_data['jobs'].items():
            doc.append(f"\n### {job_name}\n")
            
            if isinstance(job_config, dict):
                # Job name/description
                if 'name' in job_config:
                    doc.append(f"**Name:** {job_config['name']}\n\n")
                
                # Runs on
                if 'runs-on' in job_config:
                    runs_on = job_config['runs-on']
                    if isinstance(runs_on, list):
                        runs_on = ', '.join(runs_on)
                    doc.append(f"**Runs on:** `{runs_on}`\n\n")
                
                # Strategy
                if 'strategy' in job_config:
                    doc.append("**Strategy:**\n")
                    strategy = job_config['strategy']
                    if 'matrix' in strategy:
                        doc.append("- Matrix build\n")
                        for key, values in strategy['matrix'].items():
                            if isinstance(values, list):
                                doc.append(f"  - {key}: {', '.join(str(v) for v in values)}\n")
                    doc.append("\n")
                
                # Steps
                if 'steps' in job_config:
                    doc.append("**Steps:**\n\n")
                    for i, step in enumerate(job_config['steps'], 1):
                        step_name = step.get('name', f'Step {i}')
                        doc.append(f"{i}. **{step_name}**\n")
                        
                        if 'uses' in step:
                            doc.append(f"   - Uses: `{step['uses']}`\n")
                        
                        if 'run' in step:
                            run_cmd = step['run']
                            # Handle multiline commands
                            if '\n' in run_cmd:
                                lines = run_cmd.strip().split('\n')
                                if len(lines) <= 3:
                                    # Show all lines for short commands
                                    doc.append(f"   - Run:\n")
                                    for line in lines:
                                        if line.strip():
                                            doc.append(f"     ```\n     {line.strip()}\n     ```\n")
                                else:
                                    # Show first few lines for long commands
                                    doc.append(f"   - Run: Multi-line command ({len(lines)} lines)\n")
                                    doc.append(f"     ```\n")
                                    for line in lines[:3]:
                                        if line.strip():
                                            doc.append(f"     {line.strip()}\n")
                                    doc.append(f"     ...\n     ```\n")
                            else:
                                # Single line command
                                if len(run_cmd) > 100:
                                    run_cmd = run_cmd[:100] + "..."
                                doc.append(f"   - Run: `{run_cmd}`\n")
                        
                        if 'with' in step:
                            doc.append(f"   - With:\n")
                            for param, value in step['with'].items():
                                doc.append(f"     - {param}: `{value}`\n")
                        
                        doc.append("\n")
    
    return ''.join(doc)


def main():
    """Main function to process all workflows and generate documentation."""
    # Use /workspace if it exists (Docker), otherwise use current directory
    if Path('/workspace').exists():
        workspace = Path('/workspace')
    else:
        workspace = Path.cwd()
    
    workflows_dir = workspace / '.github' / 'workflows'
    docs_dir = workspace / 'docs' / 'workflows'
    
    # Create docs directory if it doesn't exist
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    if not workflows_dir.exists():
        print("No .github/workflows directory found. Nothing to document.")
        return 0
    
    # Find all workflow files
    workflow_files = list(workflows_dir.glob('*.yml')) + list(workflows_dir.glob('*.yaml'))
    
    if not workflow_files:
        print("No workflow files found in .github/workflows/")
        return 0
    
    print(f"Found {len(workflow_files)} workflow(s) to document")
    
    # Process each workflow
    for workflow_path in workflow_files:
        print(f"Processing: {workflow_path.name}")
        
        workflow_data = load_workflow(workflow_path)
        if workflow_data is None:
            continue
        
        # Generate documentation
        doc_content = generate_workflow_documentation(workflow_path, workflow_data)
        
        # Write documentation file
        doc_filename = workflow_path.stem + '.md'
        doc_path = docs_dir / doc_filename
        
        with open(doc_path, 'w') as f:
            f.write(doc_content)
        
        print(f"  → Generated: docs/workflows/{doc_filename}")
    
    # Create index file
    index_path = docs_dir / 'README.md'
    with open(index_path, 'w') as f:
        f.write("# GitHub Actions Workflows Documentation\n\n")
        f.write(f"This directory contains auto-generated documentation for all GitHub Actions workflows.\n\n")
        f.write(f"**Last Updated:** {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} UTC\n\n")
        f.write("## Workflows\n\n")
        
        for workflow_path in sorted(workflow_files):
            workflow_data = load_workflow(workflow_path)
            if workflow_data:
                workflow_name = workflow_data.get('name', workflow_path.stem)
                doc_filename = workflow_path.stem + '.md'
                f.write(f"- [{workflow_name}](./{doc_filename})\n")
    
    print(f"\n✓ Documentation generated successfully in docs/workflows/")
    return 0


if __name__ == '__main__':
    sys.exit(main())
