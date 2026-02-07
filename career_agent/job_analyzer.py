import os
from typing import List
import opik
from career_agent.models import JobPosting, UserProfile
from career_agent.llm_client import LLMClient
import json


class JobAnalyzerAgent:
    """Agent that scrapes and analyzes job postings"""
    
    def __init__(self):
        self.client = LLMClient()
    
    @opik.track(name="scrape_jobs")
    def scrape_jobs(self, role: str, industry: str, limit: int = 5) -> List[JobPosting]:
        """Simulate job scraping (in production, use real job board APIs)"""
        
        try:
            # For demo: Generate realistic job postings using LLM
            prompt = f"""Generate {limit} realistic job postings for a {role} position in the {industry} industry.

Return ONLY a JSON array (no other text) with exactly this structure:
[
  {{
    "title": "job title",
    "company": "company name",
    "required_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
    "preferred_skills": ["skill6", "skill7", "skill8"],
    "description": "brief 2-3 sentence description"
  }}
]

Make it realistic with actual tech skills and real-sounding company names."""

            jobs_data = self.client.generate_json(
                system_prompt="You are a job market analyst. Return ONLY valid JSON array, no markdown, no explanation.",
                user_prompt=prompt,
                temperature=0.7
            )
            
            # Handle if response is not a list
            if not isinstance(jobs_data, list):
                jobs_data = [jobs_data]
            
            jobs = []
            for job in jobs_data:
                # Validate required fields
                if not all(k in job for k in ["title", "company", "required_skills", "preferred_skills", "description"]):
                    continue
                    
                jobs.append(JobPosting(
                    title=job["title"],
                    company=job["company"],
                    required_skills=job["required_skills"],
                    preferred_skills=job["preferred_skills"],
                    description=job["description"],
                    url=f"https://example.com/jobs/{job['company'].lower().replace(' ', '-')}"
                ))
            
            try:
                opik.track_metric(name="jobs_scraped", value=len(jobs))
            except:
                pass
            return jobs
            
        except Exception as e:
            print(f"Error in scrape_jobs: {e}")
            # Fallback to demo mode if LLM fails
            from career_agent.demo_mode import generate_jobs
            from career_agent.models import UserProfile
            profile = UserProfile(
                name="User",
                current_role="Current",
                target_role=role,
                skills=[],
                experience_years=3,
                industry=industry
            )
            return generate_jobs(role, industry, "general")[:limit]
    
    @opik.track(name="extract_skills")
    def extract_skills_from_jobs(self, jobs: List[JobPosting]) -> dict:
        """Extract and rank skills from job postings"""
        
        skill_frequency = {}
        
        for job in jobs:
            for skill in job.required_skills:
                skill_lower = skill.lower().strip()
                skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 2
            
            for skill in job.preferred_skills:
                skill_lower = skill.lower().strip()
                skill_frequency[skill_lower] = skill_frequency.get(skill_lower, 0) + 1
        
        # Sort by frequency
        sorted_skills = dict(sorted(skill_frequency.items(), key=lambda x: x[1], reverse=True))
        
        try:
            opik.track_metric(name="unique_skills_found", value=len(sorted_skills))
            opik.track_metric(name="top_skill_frequency", value=list(sorted_skills.values())[0] if sorted_skills else 0)
        except:
            pass
        
        return sorted_skills
