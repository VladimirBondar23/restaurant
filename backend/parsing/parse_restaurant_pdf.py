"""
Minimal parser example.
- In a real scenario, point to your PDF/Word file and implement extraction (e.g., pdfplumber / python-docx).
- Here we show the structure and a simple heuristic that could be expanded.
- For the demo, we already provide a curated rules.json in ../data/rules.json
"""

import json
from pathlib import Path
from typing import List, Dict

OUTPUT = Path(__file__).resolve().parents[1] / "data" / "rules.generated.json"

def build_rules_from_snippets(snippets: List[str]) -> List[Dict]:
    rules: List[Dict] = []

    # Heuristic examples — detect concepts:
    for s in snippets:
        t = s.lower()
        if "ventilation" in t or "hood" in t:
            rules.append({
                "id": "ventilation_required",
                "category": "Safety",
                "applies_if": {"min_size_m2": 50, "max_size_m2": None, "min_seats": 20, "max_seats": None, "features": ["uses_gas"]},
                "requirement": "Install compliant kitchen ventilation and hood per Israeli standard.",
                "authority": "Ministry of Health / Fire Brigade / Municipality",
                "priority": "high",
                "source_ref": "Section 3.1 – Kitchen ventilation"
            })
        if "grease trap" in t or "grease" in t:
            rules.append({
                "id": "grease_trap",
                "category": "Environment",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": ["serves_meat"]},
                "requirement": "Install a grease trap and keep maintenance records.",
                "authority": "Municipality",
                "priority": "medium",
                "source_ref": "Appendix B – Sewer & fats"
            })
        if "gas" in t:
            rules.append({
                "id": "gas_certification",
                "category": "Safety",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": ["uses_gas"]},
                "requirement": "Annual inspection and certification by a licensed gas installer.",
                "authority": "Licensed Gas Authority / Municipality",
                "priority": "high",
                "source_ref": "Section 4 – Gas safety"
            })
        if "delivery" in t:
            rules.append({
                "id": "delivery_temp_logs",
                "category": "Health",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": ["delivery"]},
                "requirement": "Maintain food temperature logs during delivery and use suitable transport equipment.",
                "authority": "Ministry of Health",
                "priority": "low",
                "source_ref": "Section 6 – Food transport"
            })
    # De-dupe by id keeping first occurrence
    seen = set()
    uniq = []
    for r in rules:
        if r["id"] not in seen:
            uniq.append(r); seen.add(r["id"])
    return uniq

def main():
    # In a real parser: extract text from PDF/Word
    snippets = [
        "Compliant ventilation and hood in larger kitchens",
        "Grease trap connection for businesses that serve meat",
        "Gas system – inspection by licensed technician",
        "Delivery – temperature control and logs"
    ]
    rules = build_rules_from_snippets(snippets)
    OUTPUT.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rules)} rules → {OUTPUT}")

if __name__ == "__main__":
    main()
