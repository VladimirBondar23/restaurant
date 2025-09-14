Project

Title: Business Licensing Assistant (Restaurants, Israel)
Goal: Turn a short questionnaire (area, seats, features) into a personalized licensing report using an LLM, grounded by a curated ruleset derived from an official PDF.

Repository: https://github.com/VladimirBondar23/restaurant/tree/main
Demo scope: Subset of rules (ventilation, gas certification, grease trap, alcohol signage etc)



What to Run (Quick Start)

pip install -r requirements.txt

Environment (create .env at project root)

GOOGLE_API_KEY=<YOUR_GEMINI_KEY>
GEMINI_MODEL=gemini-1.5-flash
# (optional) RULES_PATH=backend/data/rules.json

Backend:
uvicorn backend.app:app --reload --port 8000

Frontend:
Open frontend/index.html




What’s Implemented

End to end: A web form sends the answers to a Python server, which matches rules and asks Gemini to write a report. If Gemini isn’t available, a built-in fallback report is shown.

Questionnaire: You enter area (m²), seats, and tick features (gas, meat, delivery, alcohol, open after 23:00, outdoor events, outdoor area).

Rule engine: Checks size/seats and selected features, then returns the rules that apply and explains why they matched.

AI report: Uses Google Gemini to turn the matched rules into a short, clear report. If there’s no API key or an error, it uses a simple automatic report instead.

Data: A small example parser script is included, and a curated rules.json built from the PDF is used.

Docs: Architecture, API, prompts, and a dev log are all in the docs/ folder.

Test: There’s a unit test for rule matching, and it works now that the rules file path is absolute.





AI dev tools used: ChatGPT, GitHub Copilot (prompts/design). ChatGPT is the best model to my opinion that is able to perform the tasks quiclky, efficiently and with minimal mistakes

Main language model: Google Gemini. Firstly I worked with OpenAI API but since I'm more familiar with gemini - I switched to it

Screenshots:

screenshots/01_questionnaire — filled form

screenshots/02_report — matched rules + AI report

screenshots/03_api_docs— FastAPI docs






How It Works

Matching: backend/matching.py loads backend/data/rules.json and filters by thresholds & features.

LLM Report: backend/llm_report.py sends {business, matched_rules} to Gemini with a strict system instruction (see /docs/prompts.md) and returns a concise, sectioned Markdown report (Summary; High/Medium/Low; Recommendations).

Fallback: If Gemini isn’t available, backend returns a deterministic, readable report so the app is always usable.



Security

environment variables are not loaded to code and GitHub




Future Work

Cover more rules: add fire safety, how many toilets/sinks are needed, accessibility rules, noise/hours limits, sidewalk seating permits, smoking areas, and when security staff is required.

Admin tools: a small dashboard to edit rules, support more business types (not just restaurants), and add basic user roles.




Key things I learned

Good prompts = clear results. Efficient use of AI can make any project development extremely fast. But you should be mindful of mistakes it makes and sometimes apply changes/debugging by yourself can solve the issues better.