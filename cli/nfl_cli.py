#!/usr/bin/env python3
"""Command line interface for the NFL toolkit."""

from __future__ import annotations

import argparse

from nfl import Graph, Executor
from nfl.distributed.executor import DistributedExecutor


def cmd_validate(args: argparse.Namespace) -> int:
    Graph.load(args.file)
    print(f"{args.file} is valid")
    return 0


def cmd_import(args: argparse.Namespace) -> int:
    import requests

    g = Graph.load(args.file)
    resp = requests.post(args.url.rstrip("/") + "/import", json=g.to_dict())
    print(resp.json())
    return 0


def cmd_exec(args: argparse.Namespace) -> int:
    g = Graph.load(args.file)
    if args.backend == "distributed":
        executor: Executor = DistributedExecutor(g)
    else:
        executor = Executor(g)
    executor.execute(args.node)
    print(f"Executed {args.node}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="nfl")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_val = sub.add_parser("validate", help="Validate a graph file")
    p_val.add_argument("file")
    p_val.set_defaults(func=cmd_validate)

    p_imp = sub.add_parser("import", help="Import a graph via the API")
    p_imp.add_argument("file")
    p_imp.add_argument("--url", default="http://localhost:8000")
    p_imp.set_defaults(func=cmd_import)

    p_exec = sub.add_parser("exec", help="Execute a node in a graph")
    p_exec.add_argument("node")
    p_exec.add_argument("--file", required=True)
    p_exec.add_argument("--backend", choices=["local", "distributed"], default="local")
    p_exec.set_defaults(func=cmd_exec)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
