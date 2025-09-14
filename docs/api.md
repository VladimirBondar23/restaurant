# API Documentation

Base URL: `http://localhost:8000`

---

## Health

**GET** `/api/health`  
Returns a simple health payload.

**Response 200**
```json
{ "ok": true, "app": "Business Licensing Assistant" }
```

---

## Match Rules

**POST** `/api/match`  
Filters the ruleset (`rules.json`) based on the provided business profile.

### Request Body
```json
{
  "size_m2": 65,
  "seats": 30,
  "features": ["uses_gas", "serves_meat"]
}
```

### Response 200
```json
{
  "matched": [
    {
      "rule": {
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
        "source_ref": "Section 3.1 – Kitchen ventilation"
      },
      "matched_reason": "size_m2 ≥ 50; seats ≥ 20; features: uses_gas"
    }
  ],
  "count": 3
}
```

### Notes
- `matched_reason` explains why each rule matched (threshold/feature conditions).
- The full ruleset path can be configured via `RULES_PATH` (defaults to `backend/data/rules.json`).

---

## Generate Report

**POST** `/api/report`  
Runs the matcher and then generates a narrative report using OpenAI (if `OPENAI_API_KEY` is set) or a deterministic fallback.

### Request Body
Same as `/api/match`

```json
{
  "size_m2": 65,
  "seats": 30,
  "features": ["uses_gas", "serves_meat"]
}
```

### Response 200
```json
{
  "report_markdown": "## Summary of Requirements (Auto-generated)\n**Business profile**: area 65 m², 30 seats, features: uses_gas, serves_meat.\n\n### High Priority\n- **Safety**: Install compliant kitchen ventilation ...\n",
  "matched_count": 3,
  "matched_ids": ["ventilation_required", "gas_certification", "grease_trap"],
  "raw_rules": [
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
      "source_ref": "Section 3.1 – Kitchen ventilation"
    }
  ]
}
```

### Behavior
- If `OPENAI_API_KEY` is **not** configured or the OpenAI call fails, the endpoint returns a structured fallback report.
- `report_markdown` is Markdown-formatted text; the frontend performs a light conversion to HTML.

---

## Error Handling

**Response 400**  
Returned if the payload is malformed (e.g., negative values).

**Response 500**  
Returned for unexpected server errors or rule loading issues.

Example error body:
```json
{ "detail": "Error message here" }
```

---

## Curl Examples

Health:
```bash
curl -s http://localhost:8000/api/health
```

Match:
```bash
curl -s -X POST http://localhost:8000/api/match   -H "Content-Type: application/json"   -d '{"size_m2":65,"seats":30,"features":["uses_gas","serves_meat"]}'
```

Report:
```bash
curl -s -X POST http://localhost:8000/api/report   -H "Content-Type: application/json"   -d '{"size_m2":65,"seats":30,"features":["uses_gas","serves_meat"]}'
```

---

## Environment & Config

- `OPENAI_API_KEY` (optional): if set, the report uses OpenAI Chat Completions.
- `OPENAI_MODEL` (optional): defaults to `gpt-4o-mini`.
- `RULES_PATH` (optional): path to the rules JSON (default `backend/data/rules.json`).

CORS: The backend enables CORS for localhost. Adjust `allow_origins` in `backend/settings.py` if needed.