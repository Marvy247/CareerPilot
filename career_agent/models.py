from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime


class UserProfile(BaseModel):
    """User's professional profile"""
    name: str
    current_role: str
    target_role: str
    skills: List[str]
    experience_years: int
    industry: str
    resume_text: Optional[str] = None


class JobPosting(BaseModel):
    """Scraped job posting data"""
    title: str
    company: str
    required_skills: List[str]
    preferred_skills: List[str]
    description: str
    url: str
    scraped_at: datetime = Field(default_factory=datetime.now)


class SkillGap(BaseModel):
    """Identified skill gap"""
    skill: str
    importance: float = Field(ge=0.0, le=1.0)
    frequency_in_jobs: int
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str


class LearningResource(BaseModel):
    """Curated learning resource"""
    title: str
    type: str  # course, article, video, project
    url: str
    estimated_hours: float
    difficulty: str  # beginner, intermediate, advanced
    relevance_score: float = Field(ge=0.0, le=1.0)
    skills_covered: List[str]


class LearningSession(BaseModel):
    """Scheduled learning session"""
    resource: LearningResource
    scheduled_time: datetime
    duration_minutes: int
    skill_target: str


class AnalysisResult(BaseModel):
    """Complete analysis result"""
    profile: UserProfile
    job_postings: List[JobPosting]
    skill_gaps: List[SkillGap]
    learning_resources: List[LearningResource]
    schedule: List[LearningSession]
    created_at: datetime = Field(default_factory=datetime.now)
