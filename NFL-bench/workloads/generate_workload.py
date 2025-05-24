#!/usr/bin/env python3
"""Generate synthetic workloads for NFL benchmarking."""
import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("out", help="Output JSON file")
    parser.add_argument("-n", "--nodes", type=int, default=10, help="Number of nodes")
    args = parser.parse_args()

    events = []
    for i in range(args.nodes):
        events.append({"id": i + 1, "action": "create", "type": "node", "value": f"N{i}"})
    for i in range(args.nodes - 1):
        events.append({"id": args.nodes + i + 1, "action": "edge", "from": f"N{i}", "to": f"N{i+1}"})

    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(events, fh, indent=2)


if __name__ == "__main__":
    main()
