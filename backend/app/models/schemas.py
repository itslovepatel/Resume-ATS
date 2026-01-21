"""
Pydantic models for API request/response schemas
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class CandidateInfo(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None


class SkillCategory(BaseModel):
    name: str
    skills: List[str]
    strength: str  # Strong, Moderate, Weak


class SkillsData(BaseModel):
    programming_languages: List[str] = []
    frameworks: List[str] = []
    tools: List[str] = []
    databases: List[str] = []
    soft_skills: List[str] = []
    other: List[str] = []
    total_count: int = 0
    skill_categories: List[SkillCategory] = []


class Project(BaseModel):
    title: str
    technologies: List[str] = []
    description: Optional[str] = None
    impact: Optional[str] = None
    score: int = 0  # 0-100


class Experience(BaseModel):
    company: Optional[str] = None
    role: Optional[str] = None
    duration: Optional[str] = None
    description: Optional[str] = None
    bullet_quality: int = 0
    has_metrics: bool = False
    action_verbs_count: int = 0


class ExperienceSummary(BaseModel):
    total_years: float = 0
    total_months: int = 0
    positions: List[Experience] = []
    overall_quality: int = 0


class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    year: Optional[str] = None
    gpa: Optional[str] = None


class DomainInfo(BaseModel):
    primary: str
    confidence: float
    secondary: Optional[str] = None
    keywords_matched: List[str] = []


class ATSIssue(BaseModel):
    type: str
    severity: str  # High, Medium, Low
    description: str
    suggestion: str


class Suggestion(BaseModel):
    category: str
    title: str
    description: str
    priority: str  # High, Medium, Low
    examples: List[str] = []


class ScoreBreakdown(BaseModel):
    keyword_relevance: int = 0
    section_completeness: int = 0
    formatting_score: int = 0
    skill_relevance: int = 0
    experience_clarity: int = 0
    project_impact: int = 0


class KeywordsAnalysis(BaseModel):
    found: List[str] = []
    missing: List[str] = []
    recommended: List[str] = []


class AnalysisResponse(BaseModel):
    success: bool
    candidate: CandidateInfo
    ats_score: int
    score_breakdown: ScoreBreakdown
    score_category: str  # Excellent, Good, Needs Improvement, Poor
    domain: DomainInfo
    skills: SkillsData
    projects: List[Project] = []
    experience: ExperienceSummary
    education: List[Education] = []
    issues: List[ATSIssue] = []
    suggestions: List[Suggestion] = []
    keywords_analysis: KeywordsAnalysis
    # OCR metadata
    parsing_method: str = "standard"  # "standard" | "ocr" | "ocr_unavailable"
    ocr_confidence: Optional[str] = None  # "low" | "medium" | "high" (only when OCR used)
