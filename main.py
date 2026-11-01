"""Library lending sample app built on the omnicode-core library.

    python main.py index                      build the symbol index (the leak scanner needs it)
    python main.py ui [--host H] [--port P]   web UI (indexes first if needed)
    python main.py serve                      MCP server on stdio (built-in tools + catalog_search)
    python main.py diagnose "question"        one reasoning turn through the Agent
    python main.py eval                       seeded-bug benchmark
"""

import argparse
import logging
import sys
from pathlib import Path

from omnicode_core.workspace import set_active_workspace

from lending_app.config import WORKSPACE


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="main.py", description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    ui = sub.add_parser("ui", help="launch the web UI")
    ui.add_argument("--host", default="127.0.0.1")
    ui.add_argument("--port", type=int, default=5000)
    sub.add_parser("index", help="index the codebase (required once before serve)")
    sub.add_parser("serve", help="run the MCP server on stdio")
    diagnose = sub.add_parser("diagnose", help="ask one question")
    diagnose.add_argument("question")
    sub.add_parser("eval", help="run the seeded-bug benchmark")
    args = parser.parse_args(argv)

    set_active_workspace(WORKSPACE)
    from lending_app import hooks, tools  # noqa: F401  (importing registers the @tool / @hook handlers)

    if args.command in ("index", "ui", "diagnose", "eval"):
        # The leak scanner fails closed without a symbol index, so build one on first use.
        # `serve` talks JSON-RPC on stdout and must not print, so it expects `index` to have run.
        logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
        from omnicode_core.container import ensure_index
        ensure_index(Path(WORKSPACE.repo.roots[0]))
        if args.command == "index":
            return 0

    if args.command == "ui":
        from omnicode_core.ui import serve_ui
        serve_ui(host=args.host, port=args.port, workspace=WORKSPACE)
    elif args.command == "serve":
        from omnicode_core.server import create_mcp_server
        create_mcp_server(WORKSPACE).run(transport="stdio")
    elif args.command == "diagnose":
        from omnicode_core.agent import Agent
        print(Agent(workspace=WORKSPACE).run(args.question))
    else:
        from eval.run_eval import run_benchmark
        return 0 if run_benchmark()["leaks"] == 0 else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
