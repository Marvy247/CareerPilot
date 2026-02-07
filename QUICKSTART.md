# Career Growth Agent - Quick Start Guide

## Installation

1. **Clone and setup**:
```bash
cd /home/marvi/Documents/Agent
pip install -r requirements.txt
```

2. **Configure API keys**:
```bash
cp .env.example .env
# Edit .env and add your keys:
# - OPENAI_API_KEY (required)
# - OPIK_API_KEY (get from https://www.comet.com/signup)
```

3. **Run demo**:
```bash
python -m career_agent.main
```

## Demo Flow

The demo will:
1. ✅ Create a sample user profile (Software Engineer → ML Engineer)
2. 🔍 Scrape 5 job postings using GPT-4
3. 📊 Extract and rank required skills
4. 🎯 Identify skill gaps with confidence scores
5. 📚 Curate learning resources (courses, articles, projects)
6. 📅 Generate a 2-week learning schedule
7. 🔬 Run Opik evaluations (hallucination detection, quality scoring)

## Opik Dashboard

After running, view your traces at: https://www.comet.com/

You'll see:
- Complete execution trace of all 4 agents
- Metrics: skills found, gaps identified, resources curated
- Evaluation scores: hallucination detection, relevance scoring
- Performance analytics: latency, token usage

## Customization

### Use your own profile:
Edit `career_agent/main.py` and modify the `UserProfile`:
```python
profile = UserProfile(
    name="Your Name",
    current_role="Your Current Role",
    target_role="Your Target Role",
    skills=["skill1", "skill2", ...],
    experience_years=X,
    industry="Your Industry"
)
```

### Adjust parameters:
- Job scraping limit: `scrape_jobs(limit=10)`
- Daily learning time: `create_schedule(daily_minutes=60)`
- Schedule duration: `create_schedule(days_ahead=30)`

## Architecture

```
CareerGrowthOrchestrator (main coordinator)
├── JobAnalyzerAgent (scrapes & extracts skills)
├── SkillGapAgent (identifies gaps with confidence)
├── ResourceCuratorAgent (finds & ranks resources)
└── SchedulerAgent (creates adaptive schedule)
```

All agents are traced with Opik for full observability.

## Hackathon Demo Tips

1. **Show Opik dashboard side-by-side** with terminal output
2. **Highlight confidence scores** - shows responsible AI
3. **Demonstrate adaptation** - run with different profiles
4. **Emphasize evaluation** - hallucination detection is key differentiator
5. **Show real-time tracing** - judges love seeing the agent "think"

## Troubleshooting

**No Opik traces?**
- Verify OPIK_API_KEY is set
- Check workspace name in Opik dashboard
- Ensure `opik.configure()` is called before agents run

**API errors?**
- Check OpenAI API key and credits
- Reduce `limit` parameter if rate limited
- Use `gpt-3.5-turbo` instead of `gpt-4` for faster/cheaper runs

**JSON parsing errors?**
- LLM sometimes returns invalid JSON
- Add retry logic or use structured outputs (OpenAI function calling)

## Next Steps

1. Add real job board integration (LinkedIn, Indeed APIs)
2. Connect to Google Calendar for actual scheduling
3. Implement user feedback loop for continuous improvement
4. Add more evaluation metrics (context recall, moderation)
5. Build web UI for better demo experience
