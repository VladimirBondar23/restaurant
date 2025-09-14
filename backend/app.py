from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import MatchInput, MatchResponse, ReportResponse
from backend.matching import match
from backend.llm_report import generate_report
from backend.settings import get_settings

app = FastAPI(title="Business Licensing Assistant", version="0.1.0")
settings = get_settings()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    key = settings.openai_api_key or ""
    masked = f"{key[:8]}…{key[-4:]}"
    return {"ok": True, "app": settings.app_name, "key_seen": masked}




@app.post("/api/match", response_model=MatchResponse)
def api_match(payload: MatchInput):
    try:
        res = match(payload)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/report", response_model=ReportResponse)
def api_report(payload: MatchInput):
    try:
        m = match(payload)
        rules = [mr.rule for mr in m.matched]
        report = generate_report(payload, rules)
        return ReportResponse(
            report_markdown=report,
            matched_count=m.count,
            matched_ids=[mr.rule.id for mr in m.matched],
            raw_rules=rules
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
