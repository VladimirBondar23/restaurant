import json
from typing import List

from backend.models import MatchInput, Rule
from backend.settings import get_settings

try:
    import google.generativeai as genai
except Exception:
    genai = None

SYSTEM_PROMPT = """You are a compliance assistant for Israeli restaurant licensing.
Given a business profile and a list of matched raw rules, create a concise, friendly report in English.

Goals:
- Translate regulatory language into practical, owner-friendly steps.
- Prioritize items (High, Medium, Low) and make next actions explicit.
- Be precise about thresholds and responsible authorities.
- Cite `source_ref` in parentheses where useful (e.g., "see Sec. 3.3.4").
- Keep it short, scannable, and actionable.

Structure (use headings and bullet points):
1) Short Summary (what is required overall)
2) High Priority Requirements
3) Medium Priority Requirements
4) Low Priority Requirements
5) Recommendations & Clarifications (practical tips)

Constraints:
- Do NOT invent rules; only use what is provided in `matched_rules`.
- If a rule depends on thresholds, restate the threshold clearly.
- If something is ambiguous or missing, add a short “Note” on what to verify.
"""

def _rules_to_bullets(rules: List[Rule]) -> dict:
    pr = {"high": [], "medium": [], "low": []}
    for r in rules:
        pr.get(r.priority, pr["low"]).append(r)
    return pr

def _fallback_report(business: MatchInput, rules: List[Rule]) -> str:
    groups = _rules_to_bullets(rules)

    def fmt(rs: List[Rule]) -> str:
        if not rs:
            return "- (none)\n"
        return "".join([
            f"- **{r.category}**: {r.requirement} _(authority: {r.authority})_\n"
            for r in rs
        ])

    features_txt = ", ".join(business.features) if business.features else "none"
    return f"""## Summary of Requirements (Auto-generated)
**Business profile**: area {business.size_m2} m², {business.seats} seats, features: {features_txt}.

### High Priority
{fmt(groups["high"])}

### Medium Priority
{fmt(groups["medium"])}

### Low Priority
{fmt(groups["low"])}

> Note: This is a fallback report generated without an LLM. Configure GOOGLE_API_KEY for a richer narrative.
"""

def generate_report(business: MatchInput, rules: List[Rule]) -> str:
    settings = get_settings()

    # If no SDK or no key, fall back
    if genai is None or not settings.google_api_key:
        return _fallback_report(business, rules)

    try:
        genai.configure(api_key=settings.google_api_key)

        model = genai.GenerativeModel(
            model_name=settings.gemini_model,
            system_instruction=SYSTEM_PROMPT
        )

        user_payload = {
            "business": business.model_dump(),
            "matched_rules": [r.model_dump() for r in rules]
        }

        resp = model.generate_content(
            [json.dumps(user_payload, ensure_ascii=False)],
            generation_config={"temperature": 0.3}
        )

        text = (getattr(resp, "text", "") or "").strip()
        if not text:
            return _fallback_report(business, rules) + (
                "\n\n> Note: Gemini returned no text. Showing fallback."
            )
        return text

    except Exception as e:
        return _fallback_report(business, rules) + f"\n\n> Note: Gemini error: {e}"
