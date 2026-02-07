# 🚀 Getting Started - Career Growth Agent

## What You Have

A complete, production-ready multi-agent AI system for career development with full Opik observability.

**Project Status**: ✅ Ready for hackathon submission

---

## Quick Start (5 Minutes)

### 1. Get API Keys (2 minutes)

**OpenAI API Key:**
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. Add $5-10 credits to your account

**Opik API Key:**
1. Go to https://www.comet.com/signup
2. Create free account
3. Navigate to Settings → API Keys
4. Copy your API key

### 2. Setup Environment (1 minute)

```bash
cd /home/marvi/Documents/Agent

# Copy environment template
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

Add your keys:
```
OPENAI_API_KEY=sk-your-key-here
OPIK_API_KEY=your-opik-key-here
OPIK_WORKSPACE=default
```

### 3. Install Dependencies (1 minute)

```bash
# Core dependencies
pip install -r requirements.txt

# UI dependencies (optional)
pip install -r requirements-ui.txt
```

### 4. Test Everything (1 minute)

```bash
python test_setup.py
```

All tests should pass ✅

---

## Run Your First Demo (1 Minute)

### CLI Demo

```bash
python -m career_agent.main
```

You'll see:
- 🔍 Job market analysis
- 🎯 Skill gap identification
- 📚 Resource curation
- 📅 Schedule creation
- ✅ Complete results

### Web UI Demo

```bash
streamlit run app.py
```

Then:
1. Fill in profile in sidebar
2. Click "Analyze Career Path"
3. Explore results in tabs
4. View visualizations

### View Opik Dashboard

1. Go to https://www.comet.com/
2. Navigate to your workspace
3. See all traces and metrics
4. Explore agent decisions

---

## What Each File Does

### Core Application
- `career_agent/models.py` - Data structures (UserProfile, SkillGap, etc.)
- `career_agent/job_analyzer.py` - Scrapes jobs, extracts skills
- `career_agent/skill_gap_agent.py` - Identifies missing skills
- `career_agent/resource_curator.py` - Finds learning resources
- `career_agent/scheduler_agent.py` - Creates learning schedule
- `career_agent/orchestrator.py` - Coordinates all agents
- `career_agent/main.py` - CLI demo entry point

### User Interfaces
- `app.py` - Streamlit web UI with visualizations

### Testing & Setup
- `test_setup.py` - Verify everything is configured correctly

### Documentation
- `README.md` - Main project documentation
- `QUICKSTART.md` - Detailed setup guide
- `PROJECT_SUMMARY.md` - Complete project overview
- `DEMO_SCRIPT.md` - Hackathon presentation script
- `PRESENTATION.md` - Slide deck outline
- `CHECKLIST.md` - Submission checklist
- `DIAGRAMS.md` - Architecture diagrams

### Configuration
- `.env.example` - Environment variables template
- `requirements.txt` - Python dependencies
- `requirements-ui.txt` - UI dependencies
- `.gitignore` - Git ignore rules
- `LICENSE` - MIT license

---

## Understanding the System

### How It Works

1. **User provides profile**: Current role → Target role + skills
2. **Job Analyzer**: Scrapes 5 job postings, extracts required skills
3. **Skill Gap Agent**: Compares user skills vs. market, identifies gaps
4. **Resource Curator**: Finds courses/articles/videos for each gap
5. **Scheduler**: Creates 2-week learning plan
6. **Opik**: Traces everything for observability

### Key Features

**Confidence Scores**: Every skill gap has importance + confidence ratings

**Hallucination Detection**: Opik verifies reasoning is grounded in data

**Adaptive Scheduling**: Adjusts based on user's completion rate

**Quality Evaluation**: LLM-as-a-judge rates resource quality

**Full Traceability**: Every decision logged in Opik dashboard

---

## Customizing for Demo

### Change the Sample Profile

Edit `career_agent/main.py`:

```python
profile = UserProfile(
    name="Your Name",
    current_role="Your Current Role",
    target_role="Your Target Role",
    skills=["skill1", "skill2", "skill3"],
    experience_years=5,
    industry="Your Industry"
)
```

### Adjust Parameters

```python
# More jobs to analyze
jobs = job_analyzer.scrape_jobs(limit=10)

# More learning time per day
schedule = scheduler.create_schedule(daily_minutes=60)

# Longer schedule
schedule = scheduler.create_schedule(days_ahead=30)
```

---

## Preparing for Demo Day

### 1. Practice Run (Day Before)

```bash
# Clear any old data
rm -rf .opik/  # if exists

# Run fresh demo
python -m career_agent.main

# Verify Opik dashboard shows traces
# Time yourself (should be ~60 seconds)
```

### 2. Setup Checklist (Morning Of)

- [ ] Laptop fully charged
- [ ] Internet connection tested
- [ ] API keys verified (`python test_setup.py`)
- [ ] Terminal windows ready
- [ ] Browser tabs open (Opik dashboard, GitHub)
- [ ] Backup plan ready (screenshots, video)

### 3. Demo Flow (5-7 Minutes)

1. **Intro** (30s): Problem + Solution
2. **Architecture** (30s): Show multi-agent system
3. **CLI Demo** (2m): Run live analysis
4. **Opik Dashboard** (1.5m): Show traces & evaluations
5. **Web UI** (1.5m): Show visualizations
6. **Wrap Up** (30s): Impact + next steps

See `DEMO_SCRIPT.md` for detailed walkthrough.

---

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### "API key not found" error
```bash
# Check .env file exists
ls -la .env

# Verify keys are set
cat .env
```

### "OpenAI API error"
- Check you have credits in your OpenAI account
- Verify API key is correct
- Try using `gpt-3.5-turbo` instead of `gpt-4`

### "Opik not logging traces"
- Verify OPIK_API_KEY is set
- Check workspace name
- Try logging in to Opik dashboard manually

### Demo runs but no output
- Check terminal for error messages
- Verify internet connection
- Try reducing `limit` parameter

---

## Next Steps

### For Hackathon Submission

1. ✅ Test everything works
2. ✅ Practice demo (5-7 minutes)
3. ✅ Create GitHub repository
4. ✅ Record backup demo video
5. ✅ Submit before deadline

### For Continued Development

1. Add real job board APIs (LinkedIn, Indeed)
2. Integrate with Google Calendar
3. Implement user feedback loop
4. Add more evaluation metrics
5. Build mobile app

### For Learning

1. Study the Opik integration patterns
2. Experiment with different prompts
3. Try different LLM models
4. Add new agents (e.g., mentor finder)
5. Improve evaluation metrics

---

## Resources

**Documentation:**
- Opik Docs: https://www.comet.com/docs/opik/
- OpenAI API: https://platform.openai.com/docs
- Streamlit: https://docs.streamlit.io/

**Hackathon:**
- Info: https://www.encodeclub.com/programmes/comet-resolution-v2-hackathon
- Submission: [Check hackathon page]

**Support:**
- GitHub Issues: [Your repo]/issues
- Email: [Your email]

---

## Tips for Success

### Technical
- Test on fresh environment before demo
- Have backup internet (phone hotspot)
- Clear Opik dashboard before demo for clean view
- Practice transitions between CLI/UI/Dashboard

### Presentation
- Show enthusiasm for your project
- Highlight Opik integration (key differentiator)
- Explain confidence scores (shows responsible AI)
- Demonstrate real-world impact

### Backup Plans
- Record demo video beforehand
- Take screenshots of successful runs
- Have printed notes
- Know your code well enough to explain without running

---

## You're Ready! 🎉

You have:
- ✅ Complete multi-agent system
- ✅ Full Opik integration
- ✅ Working CLI + Web UI
- ✅ Comprehensive documentation
- ✅ Demo script & presentation
- ✅ Test suite

**Now go win that hackathon! 🚀**

Questions? Check the other docs:
- Setup issues → `QUICKSTART.md`
- Demo prep → `DEMO_SCRIPT.md`
- Presentation → `PRESENTATION.md`
- Submission → `CHECKLIST.md`

Good luck! 🍀
