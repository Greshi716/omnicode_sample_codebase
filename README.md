# Library lending sample app

A small Java 17 codebase with three seeded bugs, plus a Python application built on the private
`omnicode-core` library. It shows how little code an application needs: a workspace definition, one
custom tool, two lifecycle hooks, and the OmniCode plugin from `../Project` for the Claude Code safety hooks.

## Layout

| Path | Purpose |
| :--- | :--- |
| `src/main/java/...` | The codebase under analysis (models, repositories, services) |
| `sql/migrations/` | Postgres schema (`LIB_*` tables) |
| `workflows/book_checkout_flow.xml` | Checkout workflow the `workflow_steps` tool reads |
| `lending_app/config.py` | Workspace, masking rules and MCP command, defined in Python |
| `lending_app/tools.py` | Custom tool `catalog_search` |
| `lending_app/hooks.py` | Library hooks (`before_prompt`, `before_tool`) |
| `.claude/settings.json` | Loads the plugin hooks from `../Project/plugins/omnicode-sdd-plugin` |
| `.mcp.json`, `.claude/settings.json` | Standard Claude Code MCP and permission/hook configuration |
| `eval/` | Seeded bugs (`bugs.json`) and the benchmark runner |

## Run

```bash
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env                                    # then set POSTGRES_PASSWORD
python main.py ui            # web UI on http://127.0.0.1:5000
python main.py serve         # MCP server on stdio (what .mcp.json launches)
python main.py diagnose "Why are on-time returns charged a fine?"
python main.py eval          # seeded-bug benchmark, writes eval/results.md
pytest
```

With Docker: run `docker_install.bat` (or `docker compose up -d --build`); it needs `POSTGRES_PASSWORD` in `.env`
and the framework folder at `../Project`. The first start indexes the codebase, then the UI is at
http://localhost:8080. The image contains the private framework: keep it local, never push it.

The leak scanner fails closed without a symbol index. `python main.py ui|diagnose|eval` build it on first use;
run `python main.py index` once before `python main.py serve` (what `.mcp.json` launches), because `serve`
speaks JSON-RPC on stdout and cannot print indexing progress.

## Seeded bugs (`eval/bugs.json`)

| Bug | Culprit | Symptom |
| :--- | :--- | :--- |
| BUG-001 | `LendingService.calculateOverdueFine` | On-time returns are charged one extra day of fine |
| BUG-002 | `InventoryService.decrementStock` | Concurrent checkouts drive stock negative |
| BUG-003 | `ReservationService.enqueueReservation` | NPE when a member has no tier |

The source carries no comments about the bugs, so the benchmark measures retrieval and not reading.
