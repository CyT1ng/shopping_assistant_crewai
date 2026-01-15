#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from .crew import ShoppingAssistantCrew


def build_inputs(args: argparse.Namespace) -> dict:
    return {
        "query": args.query,
        "budget": args.budget,
        "currency": args.currency,
        "region": args.region,
        "must_haves": args.must_haves or [],
        "nice_to_haves": args.nice_to_haves or [],
        "max_results": args.max_results,
    }


def main() -> None:
    load_dotenv()

    parser = argparse.ArgumentParser(description="CrewAI Shopping Assistant (skeleton)")
    parser.add_argument("--query", required=True, help="What you want to buy")
    parser.add_argument("--budget", type=float, default=None, help="Max budget (numeric)")
    parser.add_argument("--currency", default="USD", help="Currency code (default: USD)")
    parser.add_argument("--region", default="US", help="Region (default: US)")
    parser.add_argument("--must-haves", nargs="*", dest="must_haves", default=None)
    parser.add_argument("--nice-to-haves", nargs="*", dest="nice_to_haves", default=None)
    parser.add_argument("--max-results", type=int, default=10)
    parser.add_argument("--save-json", action="store_true", help="Save raw result to output/result.json")

    args = parser.parse_args()
    inputs = build_inputs(args)

    result = ShoppingAssistantCrew().crew().kickoff(inputs=inputs)

    print("\n=== Crew Result ===\n")
    print(result)

    if args.save_json:
        Path("output").mkdir(exist_ok=True)
        Path("output/result.json").write_text(json.dumps({"result": str(result)}, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
