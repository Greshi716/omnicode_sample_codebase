# Deployment Guide: OmniCode Sample App

This application is a standalone Java 17 service (Library Lending & Inventory System) integrated with the private **`omnicode-core`** library to provide zero-IP-leakage AI code assistance and diagnostics.

---

## 1. Architecture Overview

```
+─────────────────────────────────────────────────────────────────────────────+
|                        CONSUMER APPLICATION (THIS REPO)                      |
|                                                                             |
|   omnicode-sample-app/                                                      |
|   ├── src/main/java/com/example/library/       (Application Source Code)   |
|   ├── sql/migrations/                          (Flyway DDL Migrations)      |
|   ├── workflows/                               (XML Integration Flow)       |
|   ├── omnicode.workspace.yaml                  (App Masking Configuration)  |
|   ├── plugin.py                                (App Custom @tool & @hook)   |
|   └── main.py                                  (App Entry Point)            |
+──────────────────────────────────────┬──────────────────────────────────────+
                                       │ imports
                                       ▼
+─────────────────────────────────────────────────────────────────────────────+
|                          PRIVATE SOVEREIGN LIBRARY                          |
|                                                                             |
|   omnicode-core / omnicode-enterprise (Private Repository: ../Project)      |
|   ├── omnicode_core.workspace                  (Dynamic Parameterization)   |
|   ├── omnicode_core.tools                      (@tool Zero-Leak Gated Reg)  |
|   ├── omnicode_core.hooks                      (@hook Allow/Block/Modify)   |
|   ├── omnicode_core.storage                    (PostgreSQL / SQLite Store)  |
|   ├── omnicode_core.agent                      (Claude Headless Diagnostic) |
|   └── omnicode_mcp                             (FastMCP Stdio 8-Tool Server)|
+─────────────────────────────────────────────────────────────────────────────+
```

---

## 2. Prerequisites

- **Java**: OpenJDK 17 or higher
- **Maven**: 3.8+
- **Python**: 3.10+ (Python 3.12 recommended)
- **Database**: PostgreSQL 15+ (or SQLite local fallback)
- **Claude Code CLI** (for autonomous reasoning): Installed locally and authenticated (`claude --version` >= 2.1.300)

---

## 3. Local Development Setup

### Step 3.1: Install the Private `omnicode-core` Library

The private framework can be linked in editable mode or installed as a wheel:

```bash
# Option A: Editable install linking to the sibling private directory
pip install -e ../Project

# Option B: Install via environment variable pointing to the private repo
export OMNICODE_CORE_PATH="/path/to/Project"
pip install -r requirements.txt
```

Verify the library is accessible:
```bash
python -c "import omnicode_core; print('OmniCode Core Loaded!')"
```

### Step 3.2: Configure Application Workspace

Review [`omnicode.workspace.yaml`](./omnicode.workspace.yaml):
- **Package Prefixes**: `com.example.library` (masked to abstract tokens e.g. `Class_A`)
- **Table Patterns**: `^LIB_` (masked to `Table_1`, `Table_2`)
- **Storage Backend**: PostgreSQL (via `DATABASE_URL`) or SQLite fallback

```bash
# Set active workspace
export OMNICODE_WORKSPACE_CONFIG="./omnicode.workspace.yaml"
```

### Step 3.3: Run Database Migrations

Apply database schemas for both the sample app and the OmniCode audit store:

```bash
# Run OmniCode core state migrations (sessions, audit logs, vault)
python -m omnicode_core.storage.migrations --backend postgres

# Run sample app migrations
psql -U postgres -d library_db -f sql/migrations/V1__init_library.sql
psql -U postgres -d library_db -f sql/migrations/V2__reservations.sql
```

---

## 4. Running the Application

### Option A: Interactive CLI & Programmatic Diagnostic Agent
```bash
# Run diagnostic inquiry using omnicode-core Agent
python main.py --diagnose "Analyze why loan overdue fine is charging $1.50 extra on due date"
```

### Option B: FastMCP Stdio Server (for Claude Code / IDEs)
```bash
# Launch MCP server on stdio with zero-leak boundary active
python main.py --serve
```

When connected to Claude Code, all code structures, SQL tables, and stack traces are anonymized before reaching Claude. Code bodies are withheld and accessible strictly via the local `ask_onprem` oracle.

---

## 5. Docker Deployment

### Run Full Stack with Docker Compose

A production-ready [`docker-compose.yml`](./docker-compose.yml) is included:

```bash
# Start PostgreSQL database and Library App container
docker-compose up -d

# Check service health
docker-compose ps

# Follow logs
docker-compose logs -f sample-app
```

---

## 6. Diagnostic Benchmark Evaluation

Evaluate the AI diagnostic pipeline against the 3 seeded bugs:

```bash
python eval/run_eval.py
```

Results are saved to [`eval/results.md`](./eval/results.md).
