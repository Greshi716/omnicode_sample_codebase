# OmniCode Sample App: Library Lending & Inventory System

A standalone reference application demonstrating OmniCode's zero-code and zero-IP leakage privacy architecture on a clean Java 17 codebase.

---

## 1. Domain Architecture

The sample application models a multi-tier library lending and reservation system with:
- **Domain Models**: `Book`, `Member`, `MemberTier` (REGULAR, PREMIUM, VIP), `Loan`, `InventoryRecord`, `Reservation`.
- **Services**:
  - `LendingService`: Checkout, returns, and overdue fine calculations.
  - `InventoryService`: Stock availability and physical copy tracking.
  - `MemberService`: Registration and membership tier upgrades.
  - `ReservationService`: Priority-based queueing for high-demand titles.
- **SQL Migrations**:
  - `sql/migrations/V1__init_library.sql`: Core schema (`LIB_BOOKS`, `LIB_MEMBERS`, `LIB_INVENTORY`, `LIB_LOANS`).
  - `sql/migrations/V2__reservations.sql`: Priority queue schema (`LIB_RESERVATIONS`).
- **Integration Workflow**:
  - `workflows/book_checkout_flow.xml`: Step-by-step XML checkout state transitions.

---

## 2. Seeded Diagnostic Benchmarks (`eval/bugs.json`)

This codebase contains 3 seeded bugs for evaluating AI code diagnostic performance:

| Bug ID | Category | Culprit Method | Symptom |
| :--- | :--- | :--- | :--- |
| **BUG-001** | Calculation Defect | `LendingService.calculateOverdueFine` | Off-by-one error adds +1 day fine to on-time returns. |
| **BUG-002** | Concurrency Race Condition | `InventoryService.decrementStock` | Non-atomic check-then-act causes negative inventory (-1). |
| **BUG-003** | Null Pointer Dereference | `ReservationService.enqueueReservation` | NPE when member record has null tier in priority queue. |

---

## 3. Running with OmniCode

To analyze this repository with OmniCode:

```bash
# Set active workspace to this directory
export OMNICODE_WORKSPACE_CONFIG="./omnicode.workspace.yaml"

# Launch OmniCode MCP server
omnicode-mcp
```

All package names (`com.example.library`), tables (`LIB_BOOKS`), and class signatures are automatically pseudonymized before reaching external models.
