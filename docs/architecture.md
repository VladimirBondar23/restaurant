# System Architecture

## Overview

This project is a full-stack AI-powered assistant that helps restaurant owners understand business licensing requirements in Israel based on simple inputs like area, seating, and features (e.g. gas, meat, delivery). It uses OpenAI (or fallback logic) to generate personalized licensing reports.

## Components

[Frontend HTML/JS]
     |
     |  (HTTP)
     v
[FastAPI Backend]
 ├── /api/match  → Filter rules based on size, seats, features
 ├── /api/report → Filter rules + generate AI report
 └── Rule Engine (matching.py)
      |
      +--> rules.json (data source)
      |
      +--> OpenAI API (via llm_report.py)

## Flow

1. User fills a form in the frontend and submits.
2. Backend receives data → filters relevant licensing rules (`matching.py`).
3. If calling `/api/report`, it passes the filtered rules + business info to an LLM (`llm_report.py`).
4. LLM (or fallback) returns a report.
5. Frontend renders the report and matched rules.

## Technologies Used

Component: Frontend  
Stack / Tool: HTML + JS + CSS (vanilla)

Component: Backend  
Stack / Tool: FastAPI (Python)

Component: AI Integration  
Stack / Tool: OpenAI API (GPT-4o)

Component: Data Storage  
Stack / Tool: JSON rules file

Component: Dev Tools  
Stack / Tool: Cursor, Git, GitHub