import os
import opik
from opik.evaluation import evaluate
from career_agent.models import UserProfile, AnalysisResult
from career_agent.job_analyzer import JobAnalyzerAgent
from career_agent.skill_gap_agent import SkillGapAgent
from career_agent.resource_curator import ResourceCuratorAgent
from career_agent.scheduler_agent import SchedulerAgent
from career_agent.evaluator import CareerAgentEvaluator


class CareerGrowthOrchestrator:
    """Main orchestrator that coordinates all agents with Opik tracing"""
    
    def __init__(self):
        try:
            opik.configure(api_key=os.getenv("OPIK_API_KEY"))
        except Exception as e:
            print(f"⚠️  Opik configuration failed: {e}")
            print("   Continuing without Opik tracing...")
        
        self.job_analyzer = JobAnalyzerAgent()
        self.skill_gap_agent = SkillGapAgent()
        self.resource_curator = ResourceCuratorAgent()
        self.scheduler = SchedulerAgent()
        self.evaluator = CareerAgentEvaluator()
    
    @opik.track(
        name="career_growth_pipeline",
        tags=["production", "multi-agent"],
        metadata={"version": "0.1.0"}
    )
    def run_analysis(self, profile: UserProfile) -> AnalysisResult:
        """Run complete career growth analysis pipeline"""
        
        # Step 1: Analyze job market
        print(f"🔍 Analyzing job market for {profile.target_role}...")
        jobs = self.job_analyzer.scrape_jobs(
            role=profile.target_role,
            industry=profile.industry,
            limit=5
        )
        print(f"✓ Found {len(jobs)} job postings")
        
        # Step 2: Extract skills from jobs
        print("\n📊 Extracting skill requirements...")
        market_skills = self.job_analyzer.extract_skills_from_jobs(jobs)
        print(f"✓ Identified {len(market_skills)} unique skills")
        
        # Step 3: Identify skill gaps
        print(f"\n🎯 Analyzing skill gaps for {profile.name}...")
        skill_gaps = self.skill_gap_agent.analyze_gaps(profile, market_skills)
        print(f"✓ Found {len(skill_gaps)} skill gaps")
        
        # Step 4: Curate learning resources
        print("\n📚 Curating learning resources...")
        resources = self.resource_curator.curate_resources(skill_gaps)
        print(f"✓ Curated {len(resources)} resources")
        
        # Step 5: Create learning schedule
        print("\n📅 Creating personalized schedule...")
        schedule = self.scheduler.create_schedule(resources)
        print(f"✓ Scheduled {len(schedule)} learning sessions")
        
        result = AnalysisResult(
            profile=profile,
            job_postings=jobs,
            skill_gaps=skill_gaps,
            learning_resources=resources,
            schedule=schedule
        )
        
        # Evaluate quality with Opik
        print("\n🔬 Running Opik evaluations...")
        gap_eval = self.evaluator.evaluate_skill_gaps(skill_gaps, jobs)
        resource_eval = self.evaluator.evaluate_resources(resources, skill_gaps)
        
        print(f"  ✓ Grounding Score: {gap_eval['grounding_score']:.2%}")
        print(f"  ✓ Hallucination Rate: {gap_eval['hallucination_rate']:.2%}")
        print(f"  ✓ Overall Quality: {gap_eval['overall_quality']:.2%}")
        
        # Track overall metrics
        try:
            opik.track_metric(name="pipeline_success", value=1)
            opik.track_metric(name="total_gaps_found", value=len(skill_gaps))
            opik.track_metric(name="total_resources", value=len(resources))
            opik.track_metric(name="grounding_score", value=gap_eval['grounding_score'])
            opik.track_metric(name="hallucination_rate", value=gap_eval['hallucination_rate'])
            opik.track_metric(name="overall_quality", value=gap_eval['overall_quality'])
        except:
            pass
        
        return result, gap_eval, resource_eval
    
    def evaluate_pipeline(self, result: AnalysisResult, gap_eval: dict, resource_eval: dict):
        """Display evaluation results"""
        
        print("\n" + "="*60)
        print("🔬 OPIK EVALUATION RESULTS")
        print("="*60)
        
        print("\n📊 Skill Gap Quality:")
        print(f"   Grounding Score: {gap_eval['grounding_score']:.1%}")
        print(f"   Hallucination Rate: {gap_eval['hallucination_rate']:.1%}")
        print(f"   Avg Confidence: {gap_eval['avg_confidence']:.1%}")
        print(f"   Overall Quality: {gap_eval['overall_quality']:.1%}")
        
        print("\n📚 Resource Quality:")
        print(f"   Coverage: {resource_eval['coverage']:.1%}")
        print(f"   Avg Relevance: {resource_eval['avg_relevance']:.1%}")
        print(f"   Quality Score: {resource_eval['resource_quality']:.1%}")
        
        print("\n" + self.evaluator.get_evaluation_summary())
        print("\n" + "="*60)
    
    def display_results(self, result: AnalysisResult):
        """Display results in a demo-friendly format"""
        
        print("\n" + "="*60)
        print("📈 CAREER GROWTH ANALYSIS RESULTS")
        print("="*60)
        
        print(f"\n👤 Profile: {result.profile.name}")
        print(f"   Current: {result.profile.current_role}")
        print(f"   Target: {result.profile.target_role}")
        
        print(f"\n🎯 Top Skill Gaps:")
        for i, gap in enumerate(result.skill_gaps[:5], 1):
            print(f"   {i}. {gap.skill.title()}")
            print(f"      Importance: {gap.importance:.2f} | Confidence: {gap.confidence:.2f}")
            print(f"      Reason: {gap.reasoning}")
        
        print(f"\n📚 Recommended Resources:")
        for i, resource in enumerate(result.learning_resources[:5], 1):
            print(f"   {i}. {resource.title}")
            print(f"      Type: {resource.type} | Duration: {resource.estimated_hours}h | Difficulty: {resource.difficulty}")
            print(f"      URL: {resource.url}")
        
        print(f"\n📅 Learning Schedule (Next 7 days):")
        for i, session in enumerate(result.schedule[:7], 1):
            print(f"   {i}. {session.scheduled_time.strftime('%a, %b %d at %I:%M %p')}")
            print(f"      {session.resource.title} ({session.duration_minutes} min)")
        
        print("\n" + "="*60)
        print("🎉 View full traces and metrics in Opik dashboard!")
        print("="*60)
