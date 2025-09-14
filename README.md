# Business Licensing Assistant (Restaurants – Israel)

A small end-to-end system that helps restaurant owners understand relevant licensing requirements based on business size, seating capacity, and features (e.g., uses gas, serves meat, delivery).  
It parses a subset of a PDF/Word source into structured rules, matches them to user input, and uses an LLM to generate a clear, prioritized report.

## Quick Start

### 1) Prerequisites
- Python 3.10+
- (Optional) Node not required; frontend is vanilla HTML/JS.

### 2) Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # set your OpenAI key if you have one
