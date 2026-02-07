import streamlit as st
import os
from dotenv import load_dotenv
from career_agent.models import UserProfile
from career_agent.orchestrator import CareerGrowthOrchestrator
from career_agent.demo_mode import generate_demo_analysis
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Load environment
load_dotenv()

# Check which LLM provider is available
def get_llm_provider():
    if os.getenv("GROQ_API_KEY"):
        return "Groq Llama 3.3"
    elif os.getenv("GOOGLE_API_KEY"):
        return "Google Gemini (Free)"
    elif os.getenv("OPENAI_API_KEY"):
        return "OpenAI GPT-4"
    elif os.getenv("ANTHROPIC_API_KEY"):
        return "Anthropic Claude"
    return None

LLM_PROVIDER = get_llm_provider()

# Check if we should use demo mode
USE_DEMO_MODE = not LLM_PROVIDER or os.getenv("DEMO_MODE") == "true"

# Page config
st.set_page_config(
    page_title="CareerPilot - AI Career Coach",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(120deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .skill-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        margin: 0.2rem;
        background: #f0f2f6;
        border-radius: 20px;
        font-size: 0.9rem;
    }
    .resource-card {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        background: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: transform 0.2s;
    }
    .resource-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<h1 class="main-header">CareerPilot</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your AI Career Coach - Navigate Your Future with Confidence</p>', unsafe_allow_html=True)

if USE_DEMO_MODE:
    st.info("Demo Mode: Using pre-generated data (no API keys needed)")
elif LLM_PROVIDER:
    st.success(f"Live Mode: Using {LLM_PROVIDER}")

# Sidebar for user input
with st.sidebar:
    st.header("Your Profile")
    
    name = st.text_input("Full Name", "Alex Johnson", help="Enter your full name")
    
    col1, col2 = st.columns(2)
    with col1:
        experience = st.number_input("Years of Experience", 1, 30, 3, help="Total years in your field")
    with col2:
        industry = st.selectbox("Industry", ["Technology", "Finance", "Healthcare", "Education", "Retail", "Manufacturing"])
    
    current_role = st.text_input("Current Role", "Software Engineer", help="Your current job title")
    target_role = st.text_input("Target Role", "Senior Machine Learning Engineer", help="Your desired job title")
    
    st.subheader("Current Skills")
    st.caption("Enter one skill per line")
    skills_text = st.text_area(
        "Skills",
        "Python\nJavaScript\nReact\nSQL\nGit\nREST APIs",
        height=150,
        label_visibility="collapsed"
    )
    skills = [s.strip() for s in skills_text.split("\n") if s.strip()]
    
    st.markdown("---")
    
    # Settings
    with st.expander("Advanced Settings"):
        num_jobs = st.slider("Job postings to analyze", 3, 10, 5)
        daily_minutes = st.slider("Daily learning time (min)", 15, 120, 30)
    
    st.markdown("---")
    analyze_button = st.button("Analyze Career Path", type="primary", use_container_width=True)
    
    if USE_DEMO_MODE:
        st.info("Demo mode active - instant results!")
    
    st.markdown("---")
    st.caption("CareerPilot - Your AI Career Coach")
    st.caption("Built with Opik Observability")

# Main content
if analyze_button:
    # Create profile
    profile = UserProfile(
        name=name,
        current_role=current_role,
        target_role=target_role,
        skills=skills,
        experience_years=experience,
        industry=industry
    )
    
    # Run analysis with progress
    with st.spinner("🤖 Multi-agent system analyzing your career path..."):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        if USE_DEMO_MODE:
            status_text.text("🎬 Generating demo analysis...")
            progress_bar.progress(50)
            result = generate_demo_analysis(profile)
            # Mock evaluation scores for demo
            gap_eval = {
                "grounding_score": 0.95,
                "hallucination_rate": 0.05,
                "avg_confidence": 0.87,
                "overall_quality": 0.89
            }
            resource_eval = {
                "coverage": 0.92,
                "avg_relevance": 0.85,
                "resource_quality": 0.88
            }
            progress_bar.progress(100)
            status_text.text("✅ Demo analysis complete!")
        else:
            # Verify API keys
            if not LLM_PROVIDER:
                st.error("❌ No LLM provider configured. Please set GOOGLE_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY in .env file")
                st.stop()
            
            orchestrator = CareerGrowthOrchestrator()
            
            status_text.text("🔍 Analyzing job market...")
            progress_bar.progress(20)
            
            result, gap_eval, resource_eval = orchestrator.run_analysis(profile)
            
            progress_bar.progress(100)
            status_text.text("✅ Analysis complete!")
    
    # Display results in tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Skill Gaps", "Learning Resources", "Schedule", "Job Market", "Opik Evaluation"])
    
    with tab1:
        st.markdown("### 🎯 Skill Gap Analysis")
        st.markdown("Based on analysis of **{}** job postings in your target field".format(len(result.job_postings)))
        
        if result.skill_gaps:
            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Gaps", len(result.skill_gaps), help="Skills you need to learn")
            with col2:
                high_priority = len([g for g in result.skill_gaps if g.confidence > 0.7])
                st.metric("High Priority", high_priority, help="Gaps with >70% confidence")
            with col3:
                avg_conf = sum(g.confidence for g in result.skill_gaps) / len(result.skill_gaps)
                st.metric("Avg Confidence", f"{avg_conf:.0%}", help="Average confidence score")
            with col4:
                total_hours = sum(r.estimated_hours for r in result.learning_resources[:5])
                st.metric("Learning Hours", f"{total_hours}h", help="Estimated time for top 5 resources")
            
            st.markdown("---")
            
            # Priority chart
            gap_data = {
                "Skill": [g.skill.title() for g in result.skill_gaps[:8]],
                "Priority Score": [g.importance * g.confidence for g in result.skill_gaps[:8]],
                "Importance": [g.importance for g in result.skill_gaps[:8]],
                "Confidence": [g.confidence for g in result.skill_gaps[:8]]
            }
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=gap_data["Skill"],
                y=gap_data["Priority Score"],
                marker=dict(
                    color=gap_data["Priority Score"],
                    colorscale='Viridis',
                    showscale=True,
                    colorbar=dict(title="Priority")
                ),
                text=[f"{p:.2f}" for p in gap_data["Priority Score"]],
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Priority: %{y:.2f}<extra></extra>'
            ))
            fig.update_layout(
                title="Top Skill Gaps by Priority",
                xaxis_title="Skill",
                yaxis_title="Priority Score (Importance × Confidence)",
                height=450,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("---")
            
            # Detailed breakdown
            st.markdown("### 📊 Detailed Skill Analysis")
            for i, gap in enumerate(result.skill_gaps[:8], 1):
                with st.expander(f"**{i}. {gap.skill.title()}** - Priority: {gap.importance * gap.confidence:.2f}", expanded=(i<=3)):
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Importance", f"{gap.importance:.0%}")
                    col2.metric("Confidence", f"{gap.confidence:.0%}")
                    col3.metric("Job Frequency", f"{gap.frequency_in_jobs}/{len(result.job_postings)}")
                    col4.metric("Priority", f"{gap.importance * gap.confidence:.2f}")
                    
                    st.markdown("**Why this matters:**")
                    st.info(gap.reasoning)
    
    with tab2:
        st.markdown("### 📚 Curated Learning Resources")
        st.markdown(f"**{len(result.learning_resources)}** personalized resources ranked by relevance")
        
        if result.learning_resources:
            # Filter options
            col1, col2, col3 = st.columns(3)
            with col1:
                filter_type = st.multiselect("Type", ["course", "article", "video", "project"], default=["course", "article", "video", "project"])
            with col2:
                filter_difficulty = st.multiselect("Difficulty", ["beginner", "intermediate", "advanced"], default=["beginner", "intermediate", "advanced"])
            with col3:
                min_relevance = st.slider("Min Relevance", 0.0, 1.0, 0.0, 0.1)
            
            filtered_resources = [
                r for r in result.learning_resources 
                if r.type in filter_type 
                and r.difficulty in filter_difficulty 
                and r.relevance_score >= min_relevance
            ]
            
            st.markdown(f"Showing **{len(filtered_resources)}** resources")
            st.markdown("---")
            
            for i, resource in enumerate(filtered_resources[:10], 1):
                # Resource card
                st.markdown(f"""
                <div class="resource-card">
                    <h3 style="margin-top:0; color:#1f1f1f;">#{i} {resource.title}</h3>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Type badge
                    type_emoji = {"course": "🎓", "article": "📄", "video": "🎥", "project": "💻"}
                    st.markdown(f"{type_emoji.get(resource.type, '📚')} **{resource.type.title()}** • {resource.difficulty.title()}")
                    
                    # Skills covered
                    st.markdown("**Skills:** " + " ".join([f"`{s}`" for s in resource.skills_covered]))
                    
                    # Time estimate
                    st.markdown(f"⏱️ **Estimated Time:** {resource.estimated_hours} hours")
                    
                    # Link
                    st.link_button("🔗 View Resource", resource.url, use_container_width=False)
                
                with col2:
                    # Relevance score
                    st.metric("Relevance", f"{resource.relevance_score:.0%}")
                    
                    # Visual indicator
                    progress_color = "🟢" if resource.relevance_score > 0.8 else "🟡" if resource.relevance_score > 0.6 else "🟠"
                    st.markdown(f"{progress_color} Priority")
                
                st.markdown("---")
    
    with tab3:
        st.markdown("### 📅 Personalized Learning Schedule")
        
        if result.schedule:
            # Summary
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Sessions", len(result.schedule))
            with col2:
                total_hours = sum(s.duration_minutes for s in result.schedule) / 60
                st.metric("Total Hours", f"{total_hours:.1f}h")
            with col3:
                days = (result.schedule[-1].scheduled_time - result.schedule[0].scheduled_time).days + 1
                st.metric("Duration", f"{days} days")
            
            st.markdown("---")
            
            # Calendar view
            schedule_df = pd.DataFrame([{
                "Date": s.scheduled_time.strftime("%Y-%m-%d"),
                "Day": s.scheduled_time.strftime("%A"),
                "Time": s.scheduled_time.strftime("%I:%M %p"),
                "Resource": s.resource.title[:50] + "..." if len(s.resource.title) > 50 else s.resource.title,
                "Duration": f"{s.duration_minutes} min",
                "Skill": s.skill_target,
                "Type": s.resource.type.title()
            } for s in result.schedule[:14]])
            
            st.dataframe(
                schedule_df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
                    "Resource": st.column_config.TextColumn("Resource", width="large"),
                    "Skill": st.column_config.TextColumn("Target Skill", width="medium"),
                }
            )
            
            st.markdown("---")
            
            # Timeline visualization
            st.markdown("### 📊 Weekly Overview")
            
            # Group by week
            schedule_df['Week'] = pd.to_datetime(schedule_df['Date']).dt.isocalendar().week
            weekly_hours = schedule_df.groupby('Week')['Duration'].apply(
                lambda x: sum(int(d.split()[0]) for d in x) / 60
            ).reset_index()
            weekly_hours.columns = ['Week', 'Hours']
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=[f"Week {w}" for w in weekly_hours['Week']],
                y=weekly_hours['Hours'],
                marker_color='rgb(102, 126, 234)',
                text=[f"{h:.1f}h" for h in weekly_hours['Hours']],
                textposition='outside'
            ))
            fig.update_layout(
                title="Learning Hours per Week",
                xaxis_title="Week",
                yaxis_title="Hours",
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Skills timeline
            st.markdown("### 🎯 Skills Timeline")
            skills_timeline = schedule_df.groupby(['Date', 'Skill']).size().reset_index(name='Sessions')
            
            fig = px.scatter(
                skills_timeline,
                x='Date',
                y='Skill',
                size='Sessions',
                color='Skill',
                title="When You'll Learn Each Skill",
                height=400
            )
            fig.update_layout(showlegend=False, plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 💼 Job Market Intelligence")
        st.markdown(f"Analysis based on **{len(result.job_postings)}** recent job postings")
        
        # Market insights
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📈 Most In-Demand Skills")
            all_skills = {}
            for job in result.job_postings:
                for skill in job.required_skills:
                    all_skills[skill] = all_skills.get(skill, 0) + 2
                for skill in job.preferred_skills:
                    all_skills[skill] = all_skills.get(skill, 0) + 1
            
            top_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10]
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                y=[s[0] for s in top_skills],
                x=[s[1] for s in top_skills],
                orientation='h',
                marker_color='rgb(118, 75, 162)',
                text=[s[1] for s in top_skills],
                textposition='outside'
            ))
            fig.update_layout(
                height=400,
                xaxis_title="Frequency",
                yaxis_title="Skill",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### 🎯 Your Skill Coverage")
            
            user_has = len([s for s in top_skills if s[0].lower() in [sk.lower() for sk in profile.skills]])
            coverage = (user_has / len(top_skills)) * 100 if top_skills else 0
            
            fig = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=coverage,
                title={'text': "Market Alignment"},
                delta={'reference': 70, 'suffix': '%'},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "rgb(102, 126, 234)"},
                    'steps': [
                        {'range': [0, 40], 'color': "lightgray"},
                        {'range': [40, 70], 'color': "gray"},
                        {'range': [70, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 70
                    }
                }
            ))
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.info(f"You have **{user_has}/{len(top_skills)}** of the top in-demand skills")
        
        st.markdown("---")
        
        # Job postings
        st.markdown("### 📋 Analyzed Job Postings")
        for i, job in enumerate(result.job_postings, 1):
            with st.expander(f"**{i}. {job.title}** at {job.company}"):
                st.markdown(f"**Description:** {job.description}")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown("**Required Skills:**")
                    for skill in job.required_skills:
                        has_skill = skill.lower() in [s.lower() for s in profile.skills]
                        icon = "✅" if has_skill else "❌"
                        st.markdown(f"{icon} {skill}")
                
                with col2:
                    st.markdown("**Preferred Skills:**")
                    for skill in job.preferred_skills:
                        has_skill = skill.lower() in [s.lower() for s in profile.skills]
                        icon = "✅" if has_skill else "⭕"
                        st.markdown(f"{icon} {skill}")
                
                st.link_button("🔗 View Job Posting", job.url, use_container_width=False)
    
    with tab5:
        st.markdown("### 🔬 Opik Evaluation & Observability")
        st.markdown("Real-time quality assessment of AI agent decisions")
        
        # Hero metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            grounding = gap_eval.get("grounding_score", 0)
            st.metric(
                "Grounding Score",
                f"{grounding:.0%}",
                delta="Excellent" if grounding > 0.9 else "Good" if grounding > 0.7 else "Fair",
                help="How well recommendations are grounded in actual job data"
            )
        
        with col2:
            hallucination = gap_eval.get("hallucination_rate", 0)
            st.metric(
                "Hallucination Rate",
                f"{hallucination:.0%}",
                delta="Safe" if hallucination < 0.1 else "Warning",
                delta_color="inverse",
                help="Percentage of recommendations not based on real data"
            )
        
        with col3:
            confidence = gap_eval.get("avg_confidence", 0)
            st.metric(
                "Avg Confidence",
                f"{confidence:.0%}",
                delta="High" if confidence > 0.8 else "Medium",
                help="AI's confidence in its recommendations"
            )
        
        with col4:
            quality = gap_eval.get("overall_quality", 0)
            st.metric(
                "Overall Quality",
                f"{quality:.0%}",
                delta="Excellent" if quality > 0.8 else "Good",
                help="Combined quality score across all metrics"
            )
        
        st.markdown("---")
        
        # Detailed evaluation
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Skill Gap Evaluation")
            
            # Grounding visualization
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=grounding * 100,
                title={'text': "Data Grounding"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkgreen" if grounding > 0.9 else "orange"},
                    'steps': [
                        {'range': [0, 70], 'color': "lightgray"},
                        {'range': [70, 90], 'color': "lightyellow"},
                        {'range': [90, 100], 'color': "lightgreen"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=250)
            st.plotly_chart(fig, use_container_width=True)
            
            if grounding > 0.9:
                st.success("✅ Excellent - All recommendations grounded in job data")
            elif grounding > 0.7:
                st.info("✓ Good - Most recommendations are data-driven")
            else:
                st.warning("⚠️ Some recommendations may lack data support")
        
        with col2:
            st.markdown("#### 📚 Resource Quality")
            
            # Resource quality visualization
            coverage = resource_eval.get("coverage", 0)
            relevance = resource_eval.get("avg_relevance", 0)
            res_quality = resource_eval.get("resource_quality", 0)
            
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=['Coverage', 'Relevance', 'Overall'],
                y=[coverage * 100, relevance * 100, res_quality * 100],
                marker_color=['#667eea', '#764ba2', '#f093fb'],
                text=[f"{coverage:.0%}", f"{relevance:.0%}", f"{res_quality:.0%}"],
                textposition='outside'
            ))
            fig.update_layout(
                yaxis_title="Score (%)",
                height=250,
                showlegend=False,
                yaxis_range=[0, 110]
            )
            st.plotly_chart(fig, use_container_width=True)
            
            if res_quality > 0.8:
                st.success("✅ High-quality resources selected")
            else:
                st.info("✓ Good resource selection")
        
        st.markdown("---")
        
        # Why this matters
        st.markdown("### 🎯 Why Opik Evaluation Matters")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("#### 🛡️ Trust & Safety")
            st.markdown("""
            - Detects hallucinations
            - Verifies data grounding
            - Prevents bad recommendations
            - Ensures AI reliability
            """)
        
        with col2:
            st.markdown("#### 📈 Continuous Improvement")
            st.markdown("""
            - Tracks quality over time
            - Identifies weak points
            - Enables A/B testing
            - Optimizes prompts
            """)
        
        with col3:
            st.markdown("#### 🔍 Full Transparency")
            st.markdown("""
            - Complete trace visibility
            - Explainable decisions
            - Audit trail for compliance
            - Debug production issues
            """)
        
        st.markdown("---")
        
        # Opik dashboard link
        st.info("🔗 **View Complete Traces in Opik Dashboard**\n\nEvery agent decision, reasoning chain, and evaluation metric is logged to Opik for complete observability.")
        
        col1, col2 = st.columns(2)
        with col1:
            st.link_button("📊 Open Opik Dashboard", "https://www.comet.com/", use_container_width=True)
        with col2:
            if st.button("🔄 Refresh Evaluation", use_container_width=True):
                st.rerun()

else:
    # Welcome screen
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### Welcome to CareerPilot")
        st.markdown("""
        Your intelligent AI career coach that transforms vague goals into actionable plans.
        
        **How CareerPilot works:**
        1. Analyze - We scan the job market for your target role
        2. Identify - AI identifies your specific skill gaps with confidence scores
        3. Curate - Find the best learning resources ranked by relevance
        4. Schedule - Get a personalized learning plan that fits your life
        5. Track - Monitor your progress with full transparency
        """)
        
        st.markdown("---")
        
        # Features
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.markdown("#### Multi-Agent AI")
            st.markdown("4 specialized agents working together to analyze your career path")
        
        with col_b:
            st.markdown("#### Confidence Scores")
            st.markdown("Every recommendation includes confidence levels for transparency")
        
        with col_c:
            st.markdown("#### Full Observability")
            st.markdown("Complete tracing with Opik for trustworthy AI decisions")
    
    with col2:
        st.image("https://img.icons8.com/clouds/400/000000/career.png", width=300)
        
        st.markdown("### Get Started")
        st.markdown("""
        1. Fill in your profile in the sidebar
        2. Click "Analyze Career Path"
        3. Get instant insights!
        """)

    st.markdown("---")
    
    # Stats
    st.markdown("### 📊 What You'll Get")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("#### 5+")
        st.markdown("Job postings analyzed")
    
    with col2:
        st.markdown("#### 8-10")
        st.markdown("Skill gaps identified")
    
    with col3:
        st.markdown("#### 15+")
        st.markdown("Curated resources")
    
    with col4:
        st.markdown("#### 14 days")
        st.markdown("Learning schedule")
    
    st.markdown("---")
    
    # Footer
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p>Built for the Comet Resolution V2 Hackathon</p>
        <p>Powered by Multi-Agent AI • Opik Observability • OpenAI GPT-4</p>
    </div>
    """, unsafe_allow_html=True)
