# Architecture Diagrams

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT                                │
│  (Profile: Current Role → Target Role + Skills)             │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│           CAREER GROWTH ORCHESTRATOR                         │
│                                                              │
│  • Coordinates all agents                                   │
│  • Manages data flow                                        │
│  • Opik tracing & evaluation                                │
│  • Error handling & retries                                 │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│    JOB      │  │   SKILL     │  │  RESOURCE   │
│  ANALYZER   │  │    GAP      │  │  CURATOR    │
│   AGENT     │  │   AGENT     │  │   AGENT     │
│             │  │             │  │             │
│ • Scrape    │  │ • Compare   │  │ • Find      │
│   jobs      │  │   skills    │  │   courses   │
│ • Extract   │  │ • Calculate │  │ • Rank by   │
│   skills    │  │   gaps      │  │   quality   │
│ • Track     │  │ • Confidence│  │ • LLM-as-   │
│   frequency │  │   scores    │  │   a-judge   │
└─────────────┘  └─────────────┘  └─────────────┘
         │               │               │
         └───────────────┼───────────────┘
                         │
                         ▼
                 ┌─────────────┐
                 │  SCHEDULER  │
                 │    AGENT    │
                 │             │
                 │ • Create    │
                 │   schedule  │
                 │ • Optimize  │
                 │   timing    │
                 │ • Adapt to  │
                 │   behavior  │
                 └─────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    OUTPUT                                    │
│                                                              │
│  • Skill gaps with confidence scores                        │
│  • Curated learning resources                               │
│  • Personalized 2-week schedule                             │
│  • Complete Opik traces                                     │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

```
User Profile
    │
    ├─► Job Analyzer ──► Job Postings + Skills
    │                           │
    │                           ▼
    └──────────────────► Skill Gap Agent ──► Skill Gaps
                                │
                                ▼
                        Resource Curator ──► Learning Resources
                                │
                                ▼
                        Scheduler Agent ──► Learning Schedule
                                │
                                ▼
                        Analysis Result (Complete)
```

## Opik Integration Points

```
┌─────────────────────────────────────────────────────────────┐
│                    OPIK PLATFORM                             │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              TRACING                                │    │
│  │  • Every agent method call                         │    │
│  │  • Complete reasoning chains                       │    │
│  │  • Input/output logging                            │    │
│  │  • Execution time tracking                         │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              METRICS                                │    │
│  │  • Jobs scraped                                    │    │
│  │  • Skill gaps found                                │    │
│  │  • Resources curated                               │    │
│  │  • Confidence scores                               │    │
│  │  • Quality ratings                                 │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              EVALUATION                             │    │
│  │  • Hallucination detection                         │    │
│  │  • Context recall                                  │    │
│  │  • Quality scoring                                 │    │
│  │  • Moderation checks                               │    │
│  └────────────────────────────────────────────────────┘    │
│                                                              │
│  ┌────────────────────────────────────────────────────┐    │
│  │              OPTIMIZATION                           │    │
│  │  • A/B testing prompts                             │    │
│  │  • Performance analytics                           │    │
│  │  • Continuous improvement                          │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Agent Interaction Sequence

```
User
  │
  │ 1. Submit Profile
  ▼
Orchestrator
  │
  │ 2. Request Job Analysis
  ▼
Job Analyzer
  │ • Scrape 5 jobs
  │ • Extract skills
  │ • @opik.track()
  │
  │ 3. Return: {jobs, skills_frequency}
  ▼
Orchestrator
  │
  │ 4. Request Gap Analysis
  ▼
Skill Gap Agent
  │ • Compare skills
  │ • Calculate gaps
  │ • LLM reasoning
  │ • @opik.track()
  │
  │ 5. Return: [SkillGap, ...]
  ▼
Orchestrator
  │
  │ 6. Request Resources
  ▼
Resource Curator
  │ • Find resources
  │ • Rank by relevance
  │ • LLM-as-a-judge
  │ • @opik.track()
  │
  │ 7. Return: [LearningResource, ...]
  ▼
Orchestrator
  │
  │ 8. Request Schedule
  ▼
Scheduler Agent
  │ • Optimize timing
  │ • Create sessions
  │ • @opik.track()
  │
  │ 9. Return: [LearningSession, ...]
  ▼
Orchestrator
  │
  │ 10. Run Evaluations
  │     • Hallucination check
  │     • Quality scoring
  │
  │ 11. Return Complete Result
  ▼
User
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                        │
│                                                              │
│  ┌──────────────┐              ┌──────────────┐            │
│  │   CLI Demo   │              │  Streamlit   │            │
│  │   (main.py)  │              │   Web UI     │            │
│  └──────────────┘              └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Orchestrator (orchestrator.py)             │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │   Job    │  │  Skill   │  │ Resource │  │Scheduler │  │
│  │ Analyzer │  │   Gap    │  │ Curator  │  │  Agent   │  │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Pydantic Models (models.py)                  │  │
│  │  • UserProfile                                       │  │
│  │  • JobPosting                                        │  │
│  │  • SkillGap                                          │  │
│  │  • LearningResource                                  │  │
│  │  • LearningSession                                   │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                         │
│                                                              │
│  ┌──────────────┐              ┌──────────────┐            │
│  │   OpenAI     │              │     Opik     │            │
│  │   GPT-4      │              │  (Comet ML)  │            │
│  │              │              │              │            │
│  │ • LLM calls  │              │ • Tracing    │            │
│  │ • Reasoning  │              │ • Metrics    │            │
│  │ • Generation │              │ • Evaluation │            │
│  └──────────────┘              └──────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

## Confidence Score Calculation

```
For each skill gap:

1. Calculate Importance
   ┌─────────────────────────────────────┐
   │ importance = frequency / max_freq   │
   │                                     │
   │ Example:                            │
   │ - Skill appears in 4/5 jobs         │
   │ - Max frequency is 5                │
   │ - Importance = 4/5 = 0.8            │
   └─────────────────────────────────────┘

2. Calculate Confidence (via LLM)
   ┌─────────────────────────────────────┐
   │ LLM analyzes:                       │
   │ - User's current role               │
   │ - Target role                       │
   │ - Existing skills                   │
   │ - Skill relevance                   │
   │                                     │
   │ Returns: confidence (0-1)           │
   └─────────────────────────────────────┘

3. Calculate Priority
   ┌─────────────────────────────────────┐
   │ priority = importance × confidence  │
   │                                     │
   │ Example:                            │
   │ - Importance: 0.8                   │
   │ - Confidence: 0.9                   │
   │ - Priority: 0.72                    │
   └─────────────────────────────────────┘

4. Sort by Priority
   ┌─────────────────────────────────────┐
   │ Top gaps = highest priority first   │
   └─────────────────────────────────────┘
```

## Opik Evaluation Flow

```
Agent Decision
    │
    ├─► Trace logged to Opik
    │
    ├─► Metrics recorded
    │   • Custom metrics per agent
    │   • Performance metrics
    │
    └─► Evaluation triggered
        │
        ├─► Hallucination Detection
        │   • Compare output to context
        │   • Score: 0 (hallucinated) to 1 (grounded)
        │
        ├─► Context Recall
        │   • Check if agent remembered profile
        │   • Score: 0 (forgot) to 1 (perfect)
        │
        └─► Quality Scoring
            • LLM-as-a-judge evaluation
            • Score: 0 (poor) to 1 (excellent)
```

---

## For Presentation

Use these diagrams to:
1. Explain system architecture
2. Show data flow between agents
3. Highlight Opik integration points
4. Demonstrate evaluation process

You can:
- Draw these on a whiteboard
- Create slides with these ASCII diagrams
- Use a tool like draw.io to make them prettier
- Show them in your README on GitHub

The ASCII format makes them easy to include in documentation and presentations!
