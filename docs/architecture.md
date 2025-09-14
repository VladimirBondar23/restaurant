# System Architecture (Gemini Version)

## Overview
This project is a full‑stack AI assistant that helps restaurant owners understand business licensing requirements in Israel based on size, seating, and operational features (e.g., gas, meat, delivery, alcohol service, late hours, outdoor use). It uses **Google Gemini** for the narrative report with a deterministic fallback when the LLM is unavailable.

## Components

Frontend (HTML/JS/CSS)
  • Collects user inputs (area, seats, features)
  • Calls backend APIs and renders the markdown report + matched rules

Backend (FastAPI, Python)
  • `/api/match` — deterministic filtering of `rules.json` by thresholds and features
  • `/api/report` — runs matcher, then calls Gemini to produce a structured report (or a fallback)

Rule Engine (`backend/matching.py`)
  • Loads and evaluates `backend/data/rules.json`
  • Produces matched rules with human‑readable “matched_reason”

LLM Integration (`backend/llm_report.py`)
  • Uses `google-generativeai` (`GenerativeModel(model_name=..., system_instruction=...)`)
  • Sends the business profile + matched rules
  • Returns concise markdown or a fallback if an error occurs

Data
  • `backend/data/rules.json`: curated subset of licensing requirements (e.g., ventilation, gas certification, potable water, solid waste, CCTV, alcohol signage)

## Data Flow
1) User submits the questionnaire in the frontend.
2) Backend `/api/match` filters rules by size, seats, and selected features.
3) Backend `/api/report` sends the business profile and matched rules to Gemini using a clear system instruction (see `docs/prompts.md`).
4) Gemini returns a concise, sectioned report (Summary, High/Medium/Low, Recommendations). If Gemini fails, a deterministic fallback is returned instead.
5) Frontend renders the report and lists matched rules for transparency.

## Configuration & Environment
- `.env` (project root), loaded with `load_dotenv(find_dotenv(), override=True)`:
  - `GOOGLE_API_KEY` — your Gemini key (required for live AI)
  - `GEMINI_MODEL` — default `gemini-1.5-flash` (or `gemini-1.5-pro`)
  - `RULES_PATH` — optional custom path to rules JSON

## Technology Stack
- Frontend: HTML/JS/CSS (vanilla)
- Backend: FastAPI (Python), Pydantic models
- AI: Google Gemini via `google-generativeai`
- Data: JSON rules file
- Dev Tools: Cursor / Copilot / ChatGPT for scaffolding and prompt iteration; Git & GitHub

## Notes and Trade‑offs
- JSON storage keeps the demo simple and transparent; easy to extend to DB later.
- Fallback mode ensures demos run without API keys or during quota/runtime errors.
- The ruleset is intentionally a subset of the source PDF; see `docs/devlog.md` for planned expansions.