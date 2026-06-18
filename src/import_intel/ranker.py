"""Rank import-substitution opportunities."""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class Candidate:
    product: str
    hs_code: str
    source_country: str
    import_value_usd_m: float
    indian_capability: int
    demand_score: int
    complexity: int
    margin_score: int
    regulation_risk: int


@dataclass(frozen=True)
class RankedCandidate:
    product: str
    score: int
    status: str
    reason: str
    next_actions: tuple[str, ...]
    caution_flags: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_csv(path: str | Path) -> list[Candidate]:
    with Path(path).open(newline="", encoding="utf-8") as handle:
        rows = csv.DictReader(handle)
        return [
            Candidate(
                product=row["product"],
                hs_code=row.get("hs_code", ""),
                source_country=row.get("source_country", ""),
                import_value_usd_m=float(row.get("import_value_usd_m") or 0),
                indian_capability=int(row.get("indian_capability") or 0),
                demand_score=int(row.get("demand_score") or 0),
                complexity=int(row.get("complexity") or 0),
                margin_score=int(row.get("margin_score") or 0),
                regulation_risk=int(row.get("regulation_risk") or 0),
            )
            for row in rows
        ]


def rank_candidates(candidates: list[Candidate]) -> list[RankedCandidate]:
    return sorted((_rank(item) for item in candidates), key=lambda item: item.score, reverse=True)


def dumps_json(candidates: list[RankedCandidate]) -> str:
    return json.dumps([item.to_dict() for item in candidates], indent=2)


def _rank(candidate: Candidate) -> RankedCandidate:
    import_bonus = min(20, int(candidate.import_value_usd_m // 5))
    score = (
        20
        + candidate.indian_capability * 4
        + candidate.demand_score * 3
        + candidate.margin_score * 2
        + import_bonus
        - candidate.complexity * 3
        - candidate.regulation_risk * 3
    )
    score = max(0, min(100, score))
    status = "research-now" if score >= 70 else "watchlist" if score >= 45 else "low-priority"
    flags = _flags(candidate)
    reason = (
        f"capability={candidate.indian_capability}/10, demand={candidate.demand_score}/10, "
        f"complexity={candidate.complexity}/10, import value=${candidate.import_value_usd_m:.1f}M"
    )
    next_actions = (
        "Identify 5 Indian suppliers or factories already near this category.",
        "Estimate landed import cost versus local BOM and assembly cost.",
        "Check certification, packaging, and distribution requirements.",
    )
    return RankedCandidate(candidate.product, score, status, reason, next_actions, tuple(flags))


def _flags(candidate: Candidate) -> list[str]:
    flags: list[str] = []
    if candidate.complexity >= 8:
        flags.append("high manufacturing complexity")
    if candidate.regulation_risk >= 7:
        flags.append("regulatory or certification risk")
    if candidate.indian_capability <= 4:
        flags.append("low current local capability")
    if candidate.import_value_usd_m < 5:
        flags.append("small import market signal")
    return flags
