"""
Parser stub (example).
- Demonstrates how you'd detect concepts in the PDF/Word and produce rules.
- For the demo, we ship a curated rules.json; this stub shows how to extend extraction.
"""

import json
from pathlib import Path
from typing import List, Dict

OUTPUT = Path(__file__).resolve().parents[1] / "data" / "rules.generated.json"

def build_rules_from_snippets(snippets: List[str]) -> List[Dict]:
    rules: List[Dict] = []
    for s in snippets:
        t = s.lower()

        # Ventilation / kitchen
        if "ventilation" in t or "hood" in t:
            rules.append({
                "id": "ventilation_required",
                "category": "Safety",
                "applies_if": {"min_size_m2": 50, "max_size_m2": None, "min_seats": 20, "max_seats": None, "features": ["uses_gas"]},
                "requirement": "Install compliant kitchen ventilation and hood per Israeli standard for larger gas-using venues.",
                "authority": "Ministry of Health / Fire Brigade / Municipality",
                "priority": "high",
                "source_ref": "Kitchen ventilation"
            })

        # Grease trap
        if "grease trap" in t or "fats" in t:
            rules.append({
                "id": "grease_trap",
                "category": "Environment",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": ["serves_meat"]},
                "requirement": "Install a grease trap and keep maintenance records.",
                "authority": "Municipality",
                "priority": "medium",
                "source_ref": "Municipal sewer/fats guidance"
            })

        # Gas
        if "gas" in t:
            rules.append({
                "id": "gas_certification",
                "category": "Safety",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": ["uses_gas"]},
                "requirement": "Annual inspection/certification by a licensed gas installer.",
                "authority": "Licensed Gas Authority / Municipality",
                "priority": "high",
                "source_ref": "Gas safety"
            })

        # Delivery
        if "delivery" in t:
            rules.append({
                "id": "delivery_temp_logs",
                "category": "Health",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": ["delivery"]},
                "requirement": "Maintain food temperature logs during delivery.",
                "authority": "Ministry of Health",
                "priority": "low",
                "source_ref": "Food transport"
            })

        # Alcohol signage
        if "alcohol" in t and "sign" in t:
            rules.append({
                "id": "alcohol_signage_id_check",
                "category": "Public Safety",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": ["serves_alcohol"]},
                "requirement": "Post legal notice (dimensions and illumination) and verify ID for alcohol service.",
                "authority": "Israel Police / Municipality",
                "priority": "high",
                "source_ref": "Alcohol signage and ID check"
            })

        # CCTV
        if "cctv" in t or "camera" in t:
            for feature in (["serves_alcohol"], ["open_after_23"]):
                rules.append({
                    "id": f"cctv_specs_{'alcohol' if 'serves_alcohol' in feature else 'night'}",
                    "category": "Security",
                    "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": feature},
                    "requirement": "Install CCTV per placement/specs (FPS, retention, resolution, low-light, export, viewing).",
                    "authority": "Israel Police",
                    "priority": "high",
                    "source_ref": "Camera location/recording/retention"
                })

        # Water
        if "water" in t or "potable" in t:
            rules.append({
                "id": "potable_water_standards",
                "category": "Health",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": []},
                "requirement": "Comply with potable water system standards and MoH guidance.",
                "authority": "Ministry of Health",
                "priority": "high",
                "source_ref": "TI 1205 / TI 1525 / TI 5452; MoH"
            })

        # Waste
        if "waste" in t or "refuse" in t or "garbage" in t:
            rules.append({
                "id": "solid_waste_handling",
                "category": "Sanitation",
                "applies_if": {"min_size_m2": 0, "max_size_m2": None, "min_seats": 0, "max_seats": None, "features": []},
                "requirement": "Provide lidded containers; sanitary storage; comply with planning regulations.",
                "authority": "Municipality / MoH",
                "priority": "medium",
                "source_ref": "Solid waste handling"
            })

    # De-dupe by ID (keep first)
    seen = set()
    uniq = []
    for r in rules:
        if r["id"] not in seen:
            uniq.append(r); seen.add(r["id"])
    return uniq

def main():
    # Example: pretend we extracted these topics from the PDF
    snippets = [
        "Compliant ventilation and hood in larger kitchens",
        "Grease trap connection for businesses that serve meat",
        "Gas system – inspection by licensed technician",
        "Delivery – temperature control and logs",
        "Alcohol service sign requirements and ID verification",
        "CCTV cameras and recording specs",
        "Potable water supply standards",
        "Solid waste storage and planning compliance"
    ]
    rules = build_rules_from_snippets(snippets)
    OUTPUT.write_text(json.dumps(rules, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(rules)} rules → {OUTPUT}")

if __name__ == "__main__":
    main()
