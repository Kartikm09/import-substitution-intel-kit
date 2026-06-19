"""CLI for import substitution intelligence."""

from __future__ import annotations

import argparse
import json

from .ranker import dumps_json, load_csv, rank_candidates
from .llm import LLMConfigurationError, LLMRequestError, generate_text


def main() -> None:
    parser = argparse.ArgumentParser(description="Rank import-substitution opportunities.")
    sub = parser.add_subparsers(dest="command", required=True)
    rank = sub.add_parser("rank")
    rank.add_argument("csv_path")
    rank.add_argument("--format", choices=["text", "json"], default="text")
    rank.add_argument("--llm", action="store_true", help="Add optional Kimi/ZenMux research memo.")
    args = parser.parse_args()

    ranked = rank_candidates(load_csv(args.csv_path))
    llm_analysis = _optional_llm_analysis(args.llm, ranked)
    if args.format == "json":
        if llm_analysis:
            print(json.dumps({"candidates": [item.to_dict() for item in ranked], "llm_analysis": llm_analysis}, indent=2))
        else:
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
    if llm_analysis:
        print("\nKimi Sourcing Memo")
        print(llm_analysis)


def _optional_llm_analysis(enabled: bool, ranked: list[object]) -> str | None:
    if not enabled:
        return None
    prompt = (
        "Turn this import-substitution ranking into a practical research memo for a founder or sourcing analyst. "
        "Be realistic about missing live trade data and mark assumptions clearly.\n\n"
        f"RANKED CANDIDATES:\n{json.dumps([item.to_dict() for item in ranked[:8]], indent=2)}\n\n"
        "Return: 1) top opportunity thesis, 2) supplier discovery checklist, "
        "3) validation plan, 4) risk register, 5) first-week action plan. "
        "Keep the full answer under 350 words with compact bullets."
    )
    try:
        return generate_text(
            prompt,
            system="You are a practical sourcing and manufacturing research analyst.",
            max_tokens=6000,
        )
    except (LLMConfigurationError, LLMRequestError) as exc:
        raise SystemExit(str(exc)) from exc


if __name__ == "__main__":
    main()
