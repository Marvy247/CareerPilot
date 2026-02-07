import os
from typing import List
import opik
from career_agent.models import SkillGap, LearningResource
from career_agent.llm_client import LLMClient
import json


class ResourceCuratorAgent:
    """Agent that finds and ranks learning resources"""
    
    def __init__(self):
        self.client = LLMClient()
    
    @opik.track(name="curate_resources")
    def curate_resources(
        self, 
        skill_gaps: List[SkillGap],
        max_resources_per_skill: int = 3
    ) -> List[LearningResource]:
        """Find learning resources for each skill gap"""
        
        all_resources = []
        
        for gap in skill_gaps[:5]:  # Focus on top 5 gaps
            prompt = f"""Find {max_resources_per_skill} high-quality learning resources for: {gap.skill}

Context: User needs to learn this for career transition. Importance: {gap.importance:.2f}

For each resource provide:
- title
- type (course/article/video/project)
- url (use real platforms like Coursera, Udemy, YouTube, freeCodeCamp, etc.)
- estimated_hours (realistic estimate)
- difficulty (beginner/intermediate/advanced)
- skills_covered (list of specific skills)

Return as JSON array."""

            resources_data = self.client.generate_json(
                system_prompt="You are a learning resource curator. Return only valid JSON.",
                user_prompt=prompt,
                temperature=0.5
            )
            
            for resource in resources_data:
                all_resources.append(LearningResource(
                    title=resource["title"],
                    type=resource["type"],
                    url=resource["url"],
                    estimated_hours=resource["estimated_hours"],
                    difficulty=resource["difficulty"],
                    relevance_score=gap.importance * gap.confidence,
                    skills_covered=resource["skills_covered"]
                ))
        
        # Sort by relevance
        all_resources.sort(key=lambda x: x.relevance_score, reverse=True)
        
        try:
            opik.track_metric(name="resources_curated", value=len(all_resources))
            opik.track_metric(name="avg_relevance_score", value=sum(r.relevance_score for r in all_resources) / len(all_resources) if all_resources else 0)
        except:
            pass
        
        return all_resources
    
    @opik.track(name="evaluate_resource_quality")
    def evaluate_quality(self, resource: LearningResource) -> float:
        """Evaluate resource quality using LLM-as-a-judge"""
        
        prompt = f"""Evaluate this learning resource quality:

Title: {resource.title}
Type: {resource.type}
URL: {resource.url}
Skills: {', '.join(resource.skills_covered)}

Rate from 0-1 based on:
- Credibility of source
- Comprehensiveness
- Practical applicability

Return only a number between 0 and 1."""

        response_text = self.client.generate(
            system_prompt="You are an educational content evaluator.",
            user_prompt=prompt,
            temperature=0.2
        )
        
        quality_score = float(response_text.strip())
        try:
            opik.track_metric(name="resource_quality_score", value=quality_score)
        except:
            pass
        
        return quality_score
