import json
from typing import List
from backend.models import Rule, MatchResult, MatchResponse, MatchInput
from backend.settings import get_settings

def load_rules() -> List[Rule]:
    settings = get_settings()
    with open(settings.data_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Rule(**r) for r in data]

def _applies(rule: Rule, size: float, seats: int, features: List[str]) -> tuple[bool, str]:
    c = rule.applies_if
    reasons = []

    size_ok = True
    if c.min_size_m2 is not None:
        size_ok = size_ok and size >= c.min_size_m2
        if size >= c.min_size_m2:
            reasons.append(f"size_m2 ≥ {c.min_size_m2}")
    if c.max_size_m2 is not None:
        size_ok = size_ok and size <= c.max_size_m2
        if size <= c.max_size_m2:
            reasons.append(f"size_m2 ≤ {c.max_size_m2}")

    seats_ok = True
    if c.min_seats is not None:
        seats_ok = seats_ok and seats >= c.min_seats
        if seats >= c.min_seats:
            reasons.append(f"seats ≥ {c.min_seats}")
    if c.max_seats is not None:
        seats_ok = seats_ok and seats <= c.max_seats
        if seats <= c.max_seats:
            reasons.append(f"seats ≤ {c.max_seats}")

    features_ok = True
    if c.features:
        features_ok = all(f in features for f in c.features)
        if features_ok:
            reasons.append("features: " + ", ".join(c.features))

    ok = size_ok and seats_ok and features_ok
    return ok, "; ".join(reasons) if reasons else ""

def match(input_data: MatchInput) -> MatchResponse:
    rules = load_rules()
    matched: List[MatchResult] = []
    for r in rules:
        ok, reason = _applies(r, input_data.size_m2, input_data.seats, input_data.features)
        if ok:
            matched.append(MatchResult(rule=r, matched_reason=reason or "General applicability"))
    return MatchResponse(matched=matched, count=len(matched))
