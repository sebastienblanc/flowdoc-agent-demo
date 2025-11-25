## Example CI Workflow

Metadata:
- **Workflow File Name:** `example-ci-workflow.yml`
- **Last Generated Timestamp:** `[insert timestamp here]`

### Triggers

When this workflow is triggered, it runs based on the following events:

- **Push Events:** Triggered when a push occurs to the `main` or `develop` branches.
- **Pull Request Events:** Triggered when a pull request is opened against the `main` branch.
- **Manual Dispatch Events:** Triggered manually by selecting either of these as the trigger.

### Environment Variables

Variables defined at the workflow level include:

| Variable Name  | Value          |
|-----------------|----------------|
| ENVIRONMENT  | 'production'    |
| APP_VERSION   | '1.0.0'       |

### Jobs

#### Lint Code
- **Name:** Lint Code
- **Runs On:** ubuntu-latest
- **Steps:**
  - **Checkout code:** Uses the `actions/checkout@v4` action to fetch and clone the repository.
  - **Check shell scripts:** Runs a bash script that checks for syntax errors in `.sh` files in the `scripts` directory.
  - **Validate YAML files:** Runs a bash script that checks if there are any `.yml` or `.yaml` files in `.github/workflows` or . and validates them.

#### Build Application
- **Name:** Build Application
- **Runs On:** ubuntu-latest
- **Needs:** Lint
- **Strategy:**
  - **Matrix Builds:** Allows the build to run for multiple operating systems (currently set to `ubuntu-latest`)
- **Steps:**
  - **Checkout code:** Uses the `actions/checkout@v4` action.
  - **Display Environment Variables:** Runs a bash script that displays various environment variables.
  - **Create build artifact:** Creates a build directory and writes a `build-info.txt` file with information about the build date and version.
  - **Upload build artifacts:** Uses the `actions/upload-artifact@v4` action to upload the build artifacts.

#### Test
- **Name:** Run Tests
- **Runs On:** ubuntu-latest
- **Needs:** Build
- **Steps:**
  - **Checkout code:** Uses the `actions/checkout@v4` action.
  - **Run validation tests:** Runs a series of bash scripts to validate different aspects of the repository structure and Docker compose file syntax.

### Steps in Jobs

Below is a breakdown of each job's steps along with the actions or commands used:

#### Lint Code
- **Checkout code**
  ```sh
  uses: actions/checkout@v4
  ```
- **Check shell scripts**
  ```bash
  if ls scripts/*.sh 1> /dev/null 2>&1; then
      echo "Checking shell scripts..."
      for file in scripts/*.sh; do
          echo "Checking $file"
          bash -n "$file"
      done
  else
      echo "No shell scripts found to check"
  fi
  ```
- **Validate YAML files**
  ```bash
  echo "Checking workflow files..."
  for file in .github/workflows/*.yml .github/workflows/*.yaml; do
      if [ -f "$file" ]; then
          echo "Validating $file"
      fi
  done
  ```

#### Build Application
- **Checkout code**
  ```sh
  uses: actions/checkout@v4
  ```
- **Display environment variables**
  ```bash
  echo "Environment: ${{ env.ENVIRONMENT }}"
  echo "Version: ${{ env.APP_VERSION }}"
  echo "OS: ${{ matrix.os }}"
  ```
- **Create build artifact**
  ```sh
  mkdir -p build
  echo "Build completed at $(date)" > build/build-info.txt
  echo "Version: ${{ env.APP_VERSION }}" >> build/build-info.txt
  ```
- **Upload build artifacts**
  ```sh
  uses: actions/upload-artifact@v4
  with:
      name: build-${{ matrix.os }}
      path: build/
      retention-days: 7
  ```

#### Test
- **Checkout code**
  ```sh
  uses: actions/checkout@v4
  ```
- **Run validation tests**
  ```bash
  echo "Running validation tests..."
  test -d .github/workflows || exit 1
  test -f README.md || exit 1
  test -f compose.agent.yml || exit 1
  docker compose -f compose.agent.yml config > /dev/null 2>&1 || exit 1
  ```
- **Generate test report**
  ```bash
  mkdir -p test-results
  echo "# Test Report" > test-results/report.md
  echo "" >> test-results/report.md
  echo "## Test Summary" >> test-results/report.md
  echo "- Repository structure: ✓ PASSED" >> test-results/report.md
  echo "- Compose file validation: ✓ PASSED" >> test-results/report.md
  echo "- Test date: $(date)" >> test-results/report.md
  ```
- **Upload test results**
  ```sh
  uses: actions/upload-artifact@v4
  with:
      name: test-results
      path: test-results/
      retention-days: 7
  ```

This comprehensive documentation provides insight into the workflow's structure, triggers, environment variables, and steps for each job, helping developers understand its functionality effectively.