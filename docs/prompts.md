# Prompts (Gemini Version)

This document records the prompts and conventions the backend uses when generating tailored licensing reports with **Google Gemini**.

---

## 1) System Instruction (runtime)

You are a compliance assistant for Israeli restaurant licensing. Given a business profile and a list of matched raw rules, create a concise, friendly report in English.

Goals:
- Translate regulatory language into practical, owner‑friendly actions.
- Prioritize items (High, Medium, Low) and make next steps explicit.
- Be precise about thresholds and responsible authorities.
- Cite `source_ref` in parentheses where useful (e.g., “see Sec. 3.3.4”).
- Keep it short, scannable, and actionable.

Structure (use headings and bullets):
1) Short Summary (what is required overall)
2) High Priority Requirements
3) Medium Priority Requirements
4) Low Priority Requirements
5) Recommendations & Clarifications (practical tips)

Constraints:
- Do **not** invent rules; only use what is provided in `matched_rules`.
- If a rule depends on thresholds, restate the threshold clearly.
- If something is ambiguous or missing, add a short “Note” on what to verify.

Output format:
- Markdown headings + bullet lists.
- English only; avoid tables unless necessary.

---

## 2) Backend Payload (sent to Gemini)

```json
{
  "business": {
    "size_m2": 65.0,
    "seats": 30,
    "features": ["uses_gas", "serves_meat"]
  },
  "matched_rules": [
    {
      "id": "ventilation_required",
      "category": "Safety",
      "applies_if": {
        "min_size_m2": 50,
        "max_size_m2": null,
        "min_seats": 20,
        "max_seats": null,
        "features": ["uses_gas"]
      },
      "requirement": "Install compliant kitchen ventilation and hood per Israeli standard for businesses over 50 m² or 20 seats that use gas.",
      "authority": "Ministry of Health / Fire Brigade / Municipality",
      "priority": "high",
      "source_ref": "Kitchen ventilation (general); local standards"
    }
  ]
}
```

Notes:
- `matched_rules` is already filtered by applicability in the matcher.
- The model should present and clarify rules; do not add or remove rules.
- If no rules are matched, produce a short “No specific requirements matched” + generic guidance (e.g., contact the municipality).

---

## 3) Generation Settings (backend)

- Model: `GEMINI_MODEL` from `.env` (default: `gemini-1.5-flash`)
- Temperature: `0.3` (favor consistency and clarity)
- Call pattern (Python):  
  `GenerativeModel(model_name=..., system_instruction=SYSTEM_PROMPT).generate_content([json_payload])`

---

## 4) Assistant Style Guide (meta)

- Voice: helpful consultant, not a lawyer.
- Tone: calm, clear, direct.
- Sentences: short; bullets preferred.
- Emphasis: bold the key term in each bullet where helpful.
- Avoid hedging unless backed by data in `matched_rules`.
- Summarize the business profile once; don’t repeat it in every bullet.

---

## 5) Safety & Hallucination Controls

- The instruction forbids inventing rules not present in `matched_rules`.
- Encourage short “Note” items when information is missing/ambiguous.
- Keep temperature modest (0.2–0.3) to reduce drift.
- Use `source_ref` for light citations in parentheses where useful.

---

## 6) Example Output (outline)

```
## Summary
One paragraph highlighting the main obligations and who to contact first.

### High Priority Requirements
- **Safety — Ventilation/Hood**: action, thresholds, authority, documents, next step (see Sec. ...).

### Medium Priority Requirements
- **Environment — Grease Trap**: action and maintenance records.

### Low Priority Requirements
- (none)

### Recommendations & Clarifications
- Short tips, checks with the municipality, inspections to schedule.
```

---

## 7) Versioning

- Provider: **Google Gemini** via `google-generativeai`
- System instruction lives in `backend/llm_report.py` as `SYSTEM_PROMPT`.
- This file (`docs/prompts.md`) is the source of truth for prompt intent and structure.