# Development Log

✅ **Goals**

- Build a working end-to-end system that accepts restaurant info and returns licensing requirements.
- Focus on LLM-generated explanations.
- Use simple frontend + JSON backend without complex DB.

---

🔨 **What was built**

- `rules.json` from real-life PDF (subset for demo).
- Frontend form → calls backend → calls AI.
- Fallback reporting logic if OpenAI is unavailable.
- Match engine supports min/max + feature-based filtering.
- Markdown-to-HTML rendering in frontend.
- Git repo structured for clarity and deployment.

---

⚠️ **Challenges**

| Issue                                 | How it was solved                                          |
|--------------------------------------|-------------------------------------------------------------|
| GitHub blocked push due to secret key| Rewrote commit after removing real-looking API key         |
| LLM wasn't formatting bullets well   | Adjusted system prompt with structure hints                |
| PDF parsing was messy                | Manually extracted subset and simulated parsing            |

---

🚀 **Tools Used**

- **ChatGPT**: helped code faster with FastAPI, prompt crafting  
- **Cursor IDE**: assisted with backend-frontend syncing and refactors  
- **FastAPI**: rapid API building + built-in docs  
- **OpenAI API**: core for report generation  
- **Fallback mode**: added offline safe fallback if no API key exists

---

💡 **Improvements for Future**

- Full PDF/Word ingestion with better NLP + section recognition.  
- Add support for Hebrew report generation.  
- Make the rules editable through an admin UI.  
- Export reports as downloadable PDF.  
- Add more industries: bakeries, bars, food trucks.  
- Add login/authentication for consultants vs business owners.

---

🧠 **Key Takeaways**

- Matching rules via JSON + features is fast and works well for POC.  
- AI output quality is greatly affected by system prompts.  
- A small, focused backend is enough for powerful smart systems when combined with LLMs.