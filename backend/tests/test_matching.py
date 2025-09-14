from backend.models import MatchInput
from backend.matching import match

def test_match_gas_and_meat():
    mi = MatchInput(size_m2=60, seats=25, features=["uses_gas", "serves_meat"])
    res = match(mi)
    ids = {m.rule.id for m in res.matched}
    assert "ventilation_required" in ids
    assert "gas_certification" in ids
    assert "grease_trap" in ids

def test_match_delivery_only():
    mi = MatchInput(size_m2=20, seats=5, features=["delivery"])
    res = match(mi)
    ids = {m.rule.id for m in res.matched}
    assert "delivery_temp_logs" in ids
    assert "grease_trap" not in ids
    assert "gas_certification" not in ids
