"""Workspace definition for the library lending sample app, written in Python.

Everything organisation- or repository-specific lives here, so the omnicode-core
library itself stays generic.
"""

import os
from pathlib import Path

from omnicode_core.workspace import (
    HostConfig,
    MaskingConfig,
    RepoConfig,
    StorageConfig,
    WorkspaceConfig,
)

ROOT = Path(__file__).resolve().parent.parent

WORKSPACE = WorkspaceConfig(
    name="omnicode-sample-app",
    workspace_root=ROOT,
    repo=RepoConfig(
        roots=[str(ROOT)],
        source_roots=["src/main/java"],
        exclude=[*RepoConfig().exclude, "**/.omnicode/**", "**/eval/**", "**/.venv/**"],
    ),
    masking=MaskingConfig(
        org_terms=["LibraryCorp", "BookPlex"],
        table_patterns=["^LIB_"],
        package_prefixes=["com.example.library"],
        allowlist=["java.util", "java.time", "java.math", "java.lang"],
    ),
    workflows_dirs=["workflows"],
    docs_dirs=["README.md"],
    # Claude Code spawns the app's own entry point so the custom tool is served too.
    host=HostConfig(mcp_command=["python", "{workspace_root}/main.py", "serve"]),
    storage=StorageConfig(backend="postgres" if os.getenv("DATABASE_URL") else "sqlite"),
)
