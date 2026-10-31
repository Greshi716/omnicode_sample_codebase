# Library Lending Service — Claude Code Instructions

This project consumes the **OmniCode Spec-Driven Development (SDD) Plugin**.

---

## 1. Inherited SDD Plugin Foundation

This project operates under the **OmniCode SDD Plugin**:
- **Reasoning Workflow**: Strictly follow the 4-phase SDD lifecycle:
  1. `PLAN`: Declare hypothesis and tool roadmap before calling tools.
  2. `INVESTIGATE`: Call sovereign FastMCP tools one at a time (`search_code`, `call_graph`, `db_schema`, `workflow_steps`).
  3. `ASK_ORACLE`: Query `ask_onprem` for deep semantic code checks.
  4. `SYNTHESISE`: Produce defensive fixes and test contracts using abstract pseudonyms.
- **Privacy Guardian**: All real class names, table names, and package prefixes are masked. Never expose unmasked symbols.

---

## 2. Project-Specific Domain Rules

- **Technology Stack**: Java 17, Spring Boot 3, Flyway 10, PostgreSQL (`library_db`).
- **Architecture**:
  - `TaskTransitionCoordinator`: Concurrency and state synchronization manager.
  - `BookCatalogService`: Inventory and stock checkout operations.
  - `ReservationQueueManager`: Queue ordering and null-safe prioritization.
- **Custom Hooks**:
  - `custom_lending_guard.py`: Enforces destructive query prevention.
  - `custom_prompt_policy.py`: Blocks raw customer payment PII.

---

## 3. FastMCP Server Integration

Standard MCP configuration is declared in:
- `.mcp.json` (root standard MCP specification)
- `.claude/settings.json` (Layer 2 Claude Code settings with dual-layer hooks)
