# Example CI Workflow
**Workflow File:** `example-ci.yml`
**Last Generated:** 2025-11-24 21:36:21 UTC
---
## Triggers

### push
- **branches:**
  - `main`
  - `develop`

### pull_request
- **branches:**
  - `main`

### workflow_dispatch
- Event triggered without additional configuration

## Environment Variables
- **NODE_VERSION:** `18`
- **PYTHON_VERSION:** `3.11`

## Jobs

### build
**Name:** Build Application

**Runs on:** `ubuntu-latest`

**Strategy:**
- Matrix build
  - os: ubuntu-latest, windows-latest, macos-latest
  - node-version: 16, 18, 20

**Steps:**

1. **Checkout code**
   - Uses: `actions/checkout@v4`
   - With:
     - fetch-depth: `0`

2. **Set up Node.js**
   - Uses: `actions/setup-node@v4`
   - With:
     - node-version: `${{ matrix.node-version }}`
     - cache: `npm`

3. **Install dependencies**
   - Run: `npm ci`

4. **Run linter**
   - Run: `npm run lint`

5. **Build project**
   - Run: `npm run build`

6. **Run tests**
   - Run: `npm test`

7. **Upload build artifacts**
   - Uses: `actions/upload-artifact@v4`
   - With:
     - name: `build-${{ matrix.os }}-node-${{ matrix.node-version }}`
     - path: `dist/`
     - retention-days: `7`


### test
**Name:** Run Tests

**Runs on:** `ubuntu-latest`

**Steps:**

1. **Checkout code**
   - Uses: `actions/checkout@v4`

2. **Set up Python**
   - Uses: `actions/setup-python@v5`
   - With:
     - python-version: `${{ env.PYTHON_VERSION }}`

3. **Install Python dependencies**
   - Run:
     ```
     python -m pip install --upgrade pip
     ```
     ```
     pip install pytest pytest-cov
     ```

4. **Run Python tests**
   - Run: `pytest --cov=. --cov-report=xml`

5. **Upload coverage reports**
   - Uses: `codecov/codecov-action@v4`
   - With:
     - file: `./coverage.xml`
     - flags: `unittests`

