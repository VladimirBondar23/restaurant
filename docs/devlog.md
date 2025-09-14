# Development Log (Gemini Migration)

## 2025‑09‑14 — Switch to Gemini
- Replaced OpenAI integration with **Google Gemini**.
- Added `google-generativeai` to `requirements.txt`; removed `openai`/`httpx` pins.
- Updated `backend/llm_report.py`:
  - `GenerativeModel(model_name=..., system_instruction=...)`
  - `generate_content([json_payload], generation_config={"temperature": 0.3})`
  - Return `resp.text` with graceful fallback on exceptions.
- Updated `backend/settings.py`:
  - `.env` loading via `load_dotenv(find_dotenv(), override=True)`
  - New env vars: `GOOGLE_API_KEY`, `GEMINI_MODEL` (default `gemini-1.5-flash`)
- Updated docs in `docs/` (architecture, api, prompts, this devlog).

## Earlier — Rule Engine & Frontend
- Implemented deterministic matcher in `backend/matching.py` to filter `rules.json` by:
  - `min_size_m2`, `max_size_m2`, `min_seats`, `max_seats`
  - feature flags (e.g., `uses_gas`, `serves_meat`, `serves_alcohol`, `open_after_23`, `outdoor_events`, `has_outdoor_area`)
- Extended `rules.json` with grounded items from the source PDF (subset):
  - Ventilation, gas certification, grease trap
  - Alcohol signage/ID check, CCTV placement/specs (for alcohol/late hours)
  - Potable water standards, solid waste handling
  - External lighting for outdoor frontage, outdoor events cups
- Frontend (vanilla HTML/JS/CSS):
  - Questionnaire form + features as checkboxes
  - Calls `/api/report`, renders markdown-like output, shows matched rules

## Challenges & Fixes
- **Stale server instances** caused mixed outputs (OpenAI text still showing). Fixed by killing stray `python/uvicorn` processes and restarting on a new port.
- **Gemini SDK arg mismatch** (`model` vs `model_name`). Fixed by using `model_name`.
- **Env precedence** issues. Resolved by using `find_dotenv(..., override=True)` so `.env` wins over shell envs.
- **Secret scanning on GitHub** blocked pushes when example looked like a real key. Fixed `.env.example` to use placeholders only and rewrote commit history.

## Testing & Verification
- Manual curl tests for `/api/health`, `/api/match`, `/api/report`.
- Sanity check route (temporary) to confirm provider and masked key presence.
- Visual check in the frontend for:
  - No LLM key → fallback note appears
  - With valid Gemini key → natural, sectioned narrative appears

## Future Work
- Expand rules to cover fire protection, sanitary facility counts, accessibility, noise/hours, sidewalk seating permits, smoking areas, security staffing.
- Export PDF report; include clickable citations from `source_ref`.
- Admin UI for rule editing and threshold management.
- Optional provider switch (OpenAI/Gemini) via env for A/B comparison.
- Unit tests for rule edge cases and feature combinations.

## Tools Used
- **FastAPI**, **Pydantic**, **google-generativeai**
- **Cursor / Copilot / ChatGPT** for scaffolding and prompt iteration
- **pytest** for matcher sanity tests