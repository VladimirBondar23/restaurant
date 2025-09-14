from typing import List
from backend.models import MatchInput, Rule
from backend.settings import get_settings

# OpenAI SDK (v1)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

SYSTEM_PROMPT = """You are a compliance assistant for Israeli restaurant licensing.
Given a business profile and a list of matched raw rules, create a concise, friendly report in English:
Structure:
1) Short Summary (what is required overall)
2) High Priority Requirements
3) Medium Priority Requirements
4) Low Priority Requirements
5) Recommendations & Clarifications (practical)
For each requirement: what to do, which authority, any thresholds, documents to prepare, and next steps.
Avoid legal jargon; write for a busy owner. Keep bullet points short.
If something depends on thresholds, restate the threshold clearly.
"""

def _rules_to_bullets(rules: List[Rule]) -> dict:
    prio = {"high": [], "medium": [], "low": []}
    for r in rules:
        prio.get(r.priority, prio["low"]).append(r)
    return prio

def _fallback_report(business: MatchInput, rules: List[Rule]) -> str:
    groups = _rules_to_bullets(rules)
    def fmt(rs: List[Rule]) -> str:
        if not rs: return "- (none)\n"
        return "".join([f"- **{r.category}**: {r.requirement} _(authority: {r.authority})_\n" for r in rs])

    features_txt = ", ".join(business.features) if business.features else "none"
    return f"""## Summary of Requirements (Auto-generated)
**Business profile**: area {business.size_m2} m², {business.seats} seats, features: {features_txt}.

### High Priority
{fmt(groups["high"])}

### Medium Priority
{fmt(groups["medium"])}

### Low Priority
{fmt(groups["low"])}

> Note: This is a fallback report generated without an LLM. Provide an OpenAI API key for a richer narrative.
"""

def generate_report(business: MatchInput, rules: List[Rule]) -> str:
    settings = get_settings()
    # If no API key or SDK missing, use fallback
    if not settings.openai_api_key or OpenAI is None:
        return _fallback_report(business, rules)

    client = OpenAI(api_key=settings.openai_api_key)

    user_payload = {
        "business": business.model_dump(),
        "matched_rules": [r.model_dump() for r in rules]
    }

    content = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"JSON:\n{user_payload}"}
    ]

    try:
        resp = client.chat.completions.create(
            model=settings.openai_model,
            messages=content,
            temperature=0.3,
        )
        text = resp.choices[0].message.content.strip()
        return text
    except Exception as e:
        # Fallback on error
        return _fallback_report(business, rules) + f"\n\n> ⚠️ OpenAI error: {e}"
