import os
from typing import List
import opik
from career_agent.models import UserProfile, SkillGap
from career_agent.llm_client import LLMClient
import json


class SkillGapAgent:
    """Agent that identifies skill gaps"""
    
    def __init__(self):
        self.client = LLMClient()
    
    @opik.track(name="analyze_skill_gaps")
    def analyze_gaps(
        self, 
        profile: UserProfile, 
        market_skills: dict
    ) -> List[SkillGap]:
        """Compare user skills against market demands"""
        
        user_skills_lower = [s.lower().strip() for s in profile.skills]
        
        gaps = []
        
        for skill, frequency in market_skills.items():
            if skill not in user_skills_lower:
                # Calculate importance based on frequency
                max_freq = max(market_skills.values())
                importance = frequency / max_freq
                
                # Use LLM to assess confidence and provide reasoning
                prompt = f"""Analyze this skill gap:
                
User Profile:
- Current Role: {profile.current_role}
- Target Role: {profile.target_role}
- Experience: {profile.experience_years} years
- Current Skills: {', '.join(profile.skills)}

Missing Skill: {skill}
Frequency in job postings: {frequency}

Provide:
1. Confidence score (0-1) that this skill is truly important for their career transition
2. Brief reasoning (1 sentence)

Return as JSON: {{"confidence": 0.0-1.0, "reasoning": "..."}}"""

                result = self.client.generate_json(
                    system_prompt="You are a career advisor. Return only valid JSON.",
                    user_prompt=prompt,
                    temperature=0.3
                )
                
                gaps.append(SkillGap(
                    skill=skill,
                    importance=importance,
                    frequency_in_jobs=frequency,
                    confidence=result["confidence"],
                    reasoning=result["reasoning"]
                ))
        
        # Sort by importance * confidence
        gaps.sort(key=lambda x: x.importance * x.confidence, reverse=True)
        
        try:
            opik.track_metric(name="skill_gaps_identified", value=len(gaps))
            opik.track_metric(name="high_priority_gaps", value=len([g for g in gaps if g.confidence > 0.7]))
        except:
            pass
        
        return gaps[:10]  # Return top 10 gaps
