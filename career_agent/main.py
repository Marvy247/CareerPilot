#!/usr/bin/env python3
"""
Career Growth Agent - Demo Script
"""

import os
from dotenv import load_dotenv
from career_agent.models import UserProfile
from career_agent.orchestrator import CareerGrowthOrchestrator


def main():
    # Load environment variables
    load_dotenv()
    
    # Verify API keys
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Error: OPENAI_API_KEY not found in environment")
        print("Please create a .env file with your API keys (see .env.example)")
        return
    
    if not os.getenv("OPIK_API_KEY"):
        print("⚠️  Warning: OPIK_API_KEY not found. Opik tracing will be limited.")
    
    print("🚀 Career Growth Agent - Demo")
    print("="*60)
    
    # Create sample user profile
    profile = UserProfile(
        name="Alex Johnson",
        current_role="Software Engineer",
        target_role="Senior Machine Learning Engineer",
        skills=[
            "Python",
            "JavaScript",
            "React",
            "SQL",
            "Git",
            "REST APIs"
        ],
        experience_years=3,
        industry="Technology"
    )
    
    print(f"\n👤 User Profile:")
    print(f"   Name: {profile.name}")
    print(f"   Current Role: {profile.current_role}")
    print(f"   Target Role: {profile.target_role}")
    print(f"   Skills: {', '.join(profile.skills)}")
    print(f"   Experience: {profile.experience_years} years")
    
    # Initialize orchestrator
    orchestrator = CareerGrowthOrchestrator()
    
    # Run analysis
    print("\n" + "="*60)
    print("Starting Multi-Agent Analysis Pipeline...")
    print("="*60 + "\n")
    
    result = orchestrator.run_analysis(profile)
    
    # Display results
    orchestrator.display_results(result)
    
    # Run evaluations
    orchestrator.evaluate_pipeline(result)
    
    print("\n✅ Demo complete!")
    print("\n💡 Next steps:")
    print("   1. Check Opik dashboard for full trace visualization")
    print("   2. Review evaluation metrics and confidence scores")
    print("   3. Customize agents for your specific use case")


if __name__ == "__main__":
    main()
