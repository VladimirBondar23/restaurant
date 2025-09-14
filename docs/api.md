# API Documentation (Gemini Version)

Base URL: `http://localhost:8000`

---

## Health

**GET** `/api/health`  
Simple health check.

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
        "source_ref": "Kitchen ventilation (general); local standards"
      },
      "matched_reason": "size_m2 ≥ 50; seats ≥ 20; features: uses_gas"
    }
  ],
  "count": 3
}
```

### Notes
- `matched_reason` explains why each rule matched (thresholds/features).
- The rules file path can be configured with `RULES_PATH` (default `backend/data/rules.json`).

---

## Generate Report (Gemini)

**POST** `/api/report`  
Runs the matcher and then generates a narrative report using **Gemini** (if `GOOGLE_API_KEY` is set) or a deterministic fallback otherwise.

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
  "report_markdown": "## Summary of Requirements...",
  "matched_count": 3,
  "matched_ids": ["ventilation_required", "gas_certification", "grease_trap"],
  "raw_rules": [ { /* Rule objects */ } ]
}
```

### Behavior
- If `GOOGLE_API_KEY` is **not** configured or the Gemini call fails, the endpoint returns a structured **fallback** report.
- `report_markdown` is Markdown-formatted text; the frontend performs a light conversion to HTML.

---

## Error Handling

**Response 400** — invalid payload (e.g., negative numbers).  
**Response 500** — unexpected server errors or rule loading issues.

Example error:
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

Report (Gemini):
```bash
curl -s -X POST http://localhost:8000/api/report   -H "Content-Type: application/json"   -d '{"size_m2":65,"seats":30,"features":["uses_gas","serves_meat"]}'
```

---

## Environment & Config

- `GOOGLE_API_KEY` (required for LLM reports): your Gemini API key.
- `GEMINI_MODEL` (optional): defaults to `gemini-1.5-flash`.
- `RULES_PATH` (optional): path to the rules JSON (`backend/data/rules.json`).

CORS: The backend enables CORS for localhost. Adjust `allow_origins` in `backend/settings.py` if needed.