import os
from typing import List
from datetime import datetime, timedelta
import opik
from career_agent.models import LearningResource, LearningSession
from career_agent.llm_client import LLMClient
import json


class SchedulerAgent:
    """Agent that schedules learning sessions"""
    
    def __init__(self):
        self.client = LLMClient()
    
    @opik.track(name="create_schedule")
    def create_schedule(
        self, 
        resources: List[LearningResource],
        daily_minutes: int = 30,
        days_ahead: int = 14
    ) -> List[LearningSession]:
        """Create an adaptive learning schedule"""
        
        # Analyze user's optimal learning times (simplified for demo)
        optimal_times = self._get_optimal_times()
        
        sessions = []
        current_date = datetime.now()
        resource_index = 0
        
        for day in range(days_ahead):
            if resource_index >= len(resources):
                break
            
            # Skip weekends for demo
            schedule_date = current_date + timedelta(days=day)
            if schedule_date.weekday() >= 5:
                continue
            
            resource = resources[resource_index]
            
            # Calculate session duration
            session_duration = min(daily_minutes, resource.estimated_hours * 60)
            
            # Schedule at optimal time
            session_time = schedule_date.replace(
                hour=optimal_times[schedule_date.weekday() % len(optimal_times)],
                minute=0,
                second=0
            )
            
            sessions.append(LearningSession(
                resource=resource,
                scheduled_time=session_time,
                duration_minutes=int(session_duration),
                skill_target=resource.skills_covered[0] if resource.skills_covered else "general"
            ))
            
            # Move to next resource if current one is covered
            if session_duration >= resource.estimated_hours * 60:
                resource_index += 1
        
        try:
            opik.track_metric(name="sessions_scheduled", value=len(sessions))
            opik.track_metric(name="total_learning_hours", value=sum(s.duration_minutes for s in sessions) / 60)
        except:
            pass
        
        return sessions
    
    def _get_optimal_times(self) -> List[int]:
        """Get optimal learning times (simplified)"""
        # In production, this would analyze user's calendar and past behavior
        return [7, 19, 20, 7, 19]  # Morning or evening
    
    @opik.track(name="adapt_schedule")
    def adapt_schedule(
        self, 
        sessions: List[LearningSession],
        completion_rate: float
    ) -> List[LearningSession]:
        """Adapt schedule based on user's completion rate"""
        
        if completion_rate < 0.5:
            # User is struggling - reduce session duration
            for session in sessions:
                session.duration_minutes = int(session.duration_minutes * 0.7)
            try:
                opik.track_metric(name="schedule_adapted", value=1)
                opik.track_metric(name="adaptation_reason", value="low_completion")
            except:
                pass
        
        elif completion_rate > 0.9:
            # User is doing great - increase intensity
            for session in sessions:
                session.duration_minutes = int(session.duration_minutes * 1.3)
            try:
                opik.track_metric(name="schedule_adapted", value=1)
                opik.track_metric(name="adaptation_reason", value="high_completion")
            except:
                pass
        
        return sessions
