"""CLI for import substitution intelligence."""

from __future__ import annotations

import argparse

from .ranker import dumps_json, load_csv, rank_candidates


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank import-substitution opportunities.")
    sub = parser.add_subparsers(dest="command", required=True)
    rank = sub.add_parser("rank")
    rank.add_argument("csv_path")
    rank.add_argument("--format", choices=["text", "json"], default="text")
    args = parser.parse_args()

    ranked = rank_candidates(load_csv(args.csv_path))
    if args.format == "json":
        print(dumps_json(ranked))
        return

    print("Import Substitution Intel Kit")
    for item in ranked:
        print(f"\n{item.status.upper()} | {item.product} | score={item.score}")
        print(item.reason)
        if item.caution_flags:
            print("Cautions: " + ", ".join(item.caution_flags))
        print("Next actions:")
        for action in item.next_actions:
            print(f"- {action}")


if __name__ == "__main__":
    main()

