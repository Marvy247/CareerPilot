"""Opik evaluation metrics for the Career Growth Agent"""

import opik
from typing import List, Dict
from career_agent.models import SkillGap, JobPosting, LearningResource


class CareerAgentEvaluator:
    """Evaluates agent decisions using Opik metrics"""
    
    def __init__(self):
        self.scores = {}
    
    def evaluate_skill_gaps(self, skill_gaps: List[SkillGap], job_postings: List[JobPosting]) -> Dict:
        """Evaluate if skill gaps are grounded in actual job data"""
        
        # Extract all skills mentioned in jobs
        job_skills = set()
        for job in job_postings:
            job_skills.update([s.lower() for s in job.required_skills])
            job_skills.update([s.lower() for s in job.preferred_skills])
        
        # Check each skill gap
        grounded_count = 0
        hallucinated_count = 0
        
        for gap in skill_gaps:
            if gap.skill.lower() in job_skills:
                grounded_count += 1
            else:
                hallucinated_count += 1
        
        total = len(skill_gaps)
        grounding_score = grounded_count / total if total > 0 else 0
        
        # Calculate confidence score
        avg_confidence = sum(g.confidence for g in skill_gaps) / total if total > 0 else 0
        
        # Calculate relevance score (importance weighted)
        avg_importance = sum(g.importance for g in skill_gaps) / total if total > 0 else 0
        
        # Overall quality score
        quality_score = (grounding_score * 0.4 + avg_confidence * 0.3 + avg_importance * 0.3)
        
        self.scores = {
            "grounding_score": grounding_score,
            "hallucination_rate": hallucinated_count / total if total > 0 else 0,
            "avg_confidence": avg_confidence,
            "avg_importance": avg_importance,
            "overall_quality": quality_score,
            "grounded_gaps": grounded_count,
            "hallucinated_gaps": hallucinated_count,
            "total_gaps": total
        }
        
        return self.scores
    
    def evaluate_resources(self, resources: List[LearningResource], skill_gaps: List[SkillGap]) -> Dict:
        """Evaluate quality of curated resources"""
        
        if not resources:
            return {"resource_quality": 0, "coverage": 0}
        
        # Check coverage - do resources cover the skill gaps?
        gap_skills = set(g.skill.lower() for g in skill_gaps)
        covered_skills = set()
        
        for resource in resources:
            for skill in resource.skills_covered:
                covered_skills.add(skill.lower())
        
        coverage = len(gap_skills.intersection(covered_skills)) / len(gap_skills) if gap_skills else 0
        
        # Average relevance score
        avg_relevance = sum(r.relevance_score for r in resources) / len(resources)
        
        # Check for diverse resource types
        resource_types = set(r.type for r in resources)
        diversity_score = len(resource_types) / 4  # Max 4 types: course, article, video, project
        
        resource_quality = (avg_relevance * 0.5 + coverage * 0.3 + diversity_score * 0.2)
        
        return {
            "resource_quality": resource_quality,
            "coverage": coverage,
            "avg_relevance": avg_relevance,
            "diversity": diversity_score,
            "total_resources": len(resources)
        }
    
    def get_evaluation_summary(self) -> str:
        """Get human-readable evaluation summary"""
        if not self.scores:
            return "No evaluation performed yet"
        
        summary = []
        
        # Grounding
        grounding = self.scores.get("grounding_score", 0)
        if grounding > 0.9:
            summary.append("✅ Excellent grounding - all recommendations based on real job data")
        elif grounding > 0.7:
            summary.append("✓ Good grounding - most recommendations are data-driven")
        else:
            summary.append("⚠️ Some recommendations may not be grounded in job data")
        
        # Hallucination
        hallucination = self.scores.get("hallucination_rate", 0)
        if hallucination == 0:
            summary.append("✅ Zero hallucinations detected")
        elif hallucination < 0.2:
            summary.append("✓ Low hallucination rate - system is reliable")
        else:
            summary.append(f"⚠️ {hallucination:.0%} hallucination rate detected")
        
        # Confidence
        confidence = self.scores.get("avg_confidence", 0)
        if confidence > 0.8:
            summary.append("✅ High confidence in recommendations")
        elif confidence > 0.6:
            summary.append("✓ Moderate confidence - recommendations are reasonable")
        else:
            summary.append("⚠️ Low confidence - may need human review")
        
        # Overall
        quality = self.scores.get("overall_quality", 0)
        if quality > 0.8:
            summary.append("🎯 Overall: Excellent quality")
        elif quality > 0.6:
            summary.append("🎯 Overall: Good quality")
        else:
            summary.append("🎯 Overall: Needs improvement")
        
        return "\n".join(summary)
