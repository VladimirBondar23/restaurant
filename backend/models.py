from pydantic import BaseModel, Field
from typing import List, Optional

class MatchInput(BaseModel):
    size_m2: float = Field(..., ge=0)
    seats: int = Field(..., ge=0)
    features: List[str] = Field(default_factory=list)

class RuleCondition(BaseModel):
    min_size_m2: Optional[float] = None
    max_size_m2: Optional[float] = None
    min_seats: Optional[int] = None
    max_seats: Optional[int] = None
    features: List[str] = Field(default_factory=list)

class Rule(BaseModel):
    id: str
    category: str
    applies_if: RuleCondition
    requirement: str
    authority: str
    priority: str  # "high" | "medium" | "low"
    source_ref: Optional[str] = None  # e.g., section/page from the PDF

class MatchResult(BaseModel):
    rule: Rule
    matched_reason: str

class MatchResponse(BaseModel):
    matched: List[MatchResult]
    count: int

class ReportResponse(BaseModel):
    report_markdown: str
    matched_count: int
    matched_ids: List[str]
    raw_rules: List[Rule]
