"""Demo mode with pre-generated responses - no API keys needed"""

from datetime import datetime, timedelta
from career_agent.models import (
    JobPosting, SkillGap, LearningResource, LearningSession, AnalysisResult
)
import random


def generate_demo_analysis(profile):
    """Generate a complete demo analysis without API calls"""
    
    # Customize based on target role
    target_lower = profile.target_role.lower()
    
    # Determine focus area
    if "machine learning" in target_lower or "ml" in target_lower or "ai" in target_lower:
        focus = "ml"
    elif "data" in target_lower:
        focus = "data"
    elif "backend" in target_lower or "api" in target_lower:
        focus = "backend"
    elif "frontend" in target_lower or "react" in target_lower:
        focus = "frontend"
    elif "devops" in target_lower or "cloud" in target_lower:
        focus = "devops"
    else:
        focus = "general"
    
    # Generate relevant jobs
    jobs = generate_jobs(profile.target_role, profile.industry, focus)
    
    # Generate skill gaps
    gaps = generate_skill_gaps(profile, focus)
    
    # Generate resources
    resources = generate_resources(gaps, focus)
    
    # Generate schedule
    schedule = generate_schedule(resources)
    
    return AnalysisResult(
        profile=profile,
        job_postings=jobs,
        skill_gaps=gaps,
        learning_resources=resources,
        schedule=schedule
    )


def generate_jobs(target_role, industry, focus):
    """Generate realistic job postings"""
    
    companies = ["TechCorp", "DataCo", "StartupXYZ", "ResearchLabs", "BigTech Inc", "InnovateSoft", "CloudSystems", "AI Dynamics"]
    
    skill_sets = {
        "ml": {
            "required": ["Python", "Machine Learning", "Deep Learning", "PyTorch", "TensorFlow", "Statistics", "SQL", "Git"],
            "preferred": ["MLOps", "AWS", "Docker", "Kubernetes", "Spark", "NLP", "Computer Vision"]
        },
        "data": {
            "required": ["Python", "SQL", "Data Analysis", "Statistics", "Pandas", "NumPy", "Visualization", "Git"],
            "preferred": ["Tableau", "Power BI", "Spark", "AWS", "Machine Learning", "ETL"]
        },
        "backend": {
            "required": ["Python", "Java", "SQL", "REST APIs", "Microservices", "Git", "Docker", "Testing"],
            "preferred": ["Kubernetes", "AWS", "Redis", "GraphQL", "gRPC", "CI/CD"]
        },
        "frontend": {
            "required": ["JavaScript", "React", "HTML", "CSS", "TypeScript", "Git", "REST APIs", "Testing"],
            "preferred": ["Next.js", "Vue", "Redux", "Webpack", "GraphQL", "UI/UX"]
        },
        "devops": {
            "required": ["Linux", "Docker", "Kubernetes", "CI/CD", "AWS", "Git", "Python", "Terraform"],
            "preferred": ["Ansible", "Jenkins", "Prometheus", "Grafana", "Helm", "ArgoCD"]
        },
        "general": {
            "required": ["Python", "JavaScript", "SQL", "Git", "REST APIs", "Testing", "Agile", "Problem Solving"],
            "preferred": ["Docker", "AWS", "React", "CI/CD", "Microservices", "System Design"]
        }
    }
    
    skills = skill_sets.get(focus, skill_sets["general"])
    
    jobs = []
    for i in range(5):
        company = companies[i]
        
        # Vary the title slightly
        title_variations = [target_role, f"Senior {target_role}", f"{target_role} II", f"Lead {target_role}", target_role]
        title = title_variations[i]
        
        # Select random skills
        required = random.sample(skills["required"], min(7, len(skills["required"])))
        preferred = random.sample(skills["preferred"], min(4, len(skills["preferred"])))
        
        descriptions = [
            f"Build and deploy cutting-edge solutions at scale. Work with modern technology stack in a fast-paced environment.",
            f"Join our team to develop innovative products. Strong technical skills and collaborative mindset required.",
            f"Lead technical initiatives and mentor junior engineers. Experience with production systems essential.",
            f"Design and implement scalable solutions. Work on challenging problems with significant business impact.",
            f"Drive technical excellence in a growing team. Opportunity to shape architecture and best practices."
        ]
        
        jobs.append(JobPosting(
            title=title,
            company=company,
            required_skills=required,
            preferred_skills=preferred,
            description=descriptions[i],
            url=f"https://careers.example.com/{company.lower().replace(' ', '-')}/{i+1}"
        ))
    
    return jobs


def generate_skill_gaps(profile, focus):
    """Generate realistic skill gaps"""
    
    user_skills_lower = [s.lower() for s in profile.skills]
    
    gap_templates = {
        "ml": [
            ("Machine Learning", 1.0, 5, 0.95, "Essential for ML roles - core requirement across all positions"),
            ("Deep Learning", 0.9, 5, 0.92, "Critical for modern ML - neural networks are industry standard"),
            ("PyTorch", 0.85, 4, 0.88, "Leading deep learning framework - highly valued by employers"),
            ("TensorFlow", 0.75, 4, 0.85, "Alternative framework - broadens your toolkit"),
            ("MLOps", 0.70, 3, 0.82, "Production ML skills - bridges development and deployment"),
            ("Statistics", 0.65, 3, 0.88, "Mathematical foundation - essential for understanding algorithms"),
            ("Docker", 0.60, 3, 0.75, "Containerization standard - required for ML deployment"),
            ("AWS", 0.55, 2, 0.78, "Cloud platform skills - many companies deploy on AWS"),
            ("Kubernetes", 0.50, 2, 0.72, "Container orchestration - advanced but valuable for scaling"),
            ("NLP", 0.45, 2, 0.70, "Natural language processing - growing demand in AI applications"),
        ],
        "data": [
            ("Data Analysis", 1.0, 5, 0.95, "Core skill for data roles - fundamental requirement"),
            ("SQL", 0.95, 5, 0.93, "Database querying essential - used daily in data work"),
            ("Python", 0.90, 5, 0.92, "Primary programming language - versatile and powerful"),
            ("Statistics", 0.85, 4, 0.90, "Statistical methods crucial - foundation of data science"),
            ("Pandas", 0.80, 4, 0.87, "Data manipulation library - industry standard for Python"),
            ("Visualization", 0.75, 4, 0.85, "Communicating insights - critical for stakeholder impact"),
            ("Machine Learning", 0.70, 3, 0.80, "Predictive modeling - increasingly expected in data roles"),
            ("Tableau", 0.60, 3, 0.75, "BI tool proficiency - common in enterprise environments"),
            ("Spark", 0.55, 2, 0.72, "Big data processing - valuable for large-scale analytics"),
            ("ETL", 0.50, 2, 0.70, "Data pipeline skills - important for data engineering aspects"),
        ],
        "general": [
            ("System Design", 0.85, 4, 0.88, "Architecture skills - essential for senior roles"),
            ("Microservices", 0.80, 4, 0.85, "Modern architecture pattern - widely adopted"),
            ("Docker", 0.75, 4, 0.83, "Containerization - standard in modern development"),
            ("AWS", 0.70, 3, 0.80, "Cloud platform - most common deployment target"),
            ("CI/CD", 0.65, 3, 0.78, "Automation practices - improves development velocity"),
            ("Testing", 0.60, 3, 0.82, "Quality assurance - critical for production code"),
            ("Kubernetes", 0.55, 2, 0.72, "Container orchestration - valuable for scalability"),
            ("GraphQL", 0.50, 2, 0.68, "API technology - modern alternative to REST"),
            ("Redis", 0.45, 2, 0.65, "Caching solution - improves application performance"),
            ("Monitoring", 0.40, 2, 0.70, "Observability - essential for production systems"),
        ]
    }
    
    templates = gap_templates.get(focus, gap_templates["general"])
    
    gaps = []
    for skill, importance, freq, confidence, reasoning in templates:
        if skill.lower() not in user_skills_lower:
            gaps.append(SkillGap(
                skill=skill,
                importance=importance,
                frequency_in_jobs=freq,
                confidence=confidence,
                reasoning=reasoning
            ))
    
    return gaps[:10]


def generate_resources(gaps, focus):
    """Generate realistic learning resources"""
    
    resources = []
    
    for gap in gaps[:8]:
        skill = gap.skill.lower()
        
        # Course
        courses = {
            "machine learning": ("Machine Learning Specialization by Andrew Ng", "https://www.coursera.org/specializations/machine-learning-introduction", 60, "beginner"),
            "deep learning": ("Deep Learning Specialization", "https://www.coursera.org/specializations/deep-learning", 80, "intermediate"),
            "pytorch": ("PyTorch for Deep Learning & AI", "https://www.udemy.com/course/pytorch-for-deep-learning/", 40, "intermediate"),
            "tensorflow": ("TensorFlow Developer Certificate", "https://www.coursera.org/professional-certificates/tensorflow-in-practice", 50, "intermediate"),
            "mlops": ("MLOps Fundamentals", "https://www.coursera.org/learn/mlops-fundamentals", 25, "advanced"),
            "docker": ("Docker Mastery", "https://www.udemy.com/course/docker-mastery/", 20, "beginner"),
            "aws": ("AWS Certified Solutions Architect", "https://aws.amazon.com/certification/certified-solutions-architect-associate/", 40, "intermediate"),
            "kubernetes": ("Kubernetes for Developers", "https://www.udemy.com/course/kubernetes-for-developers/", 30, "intermediate"),
            "sql": ("Complete SQL Bootcamp", "https://www.udemy.com/course/the-complete-sql-bootcamp/", 15, "beginner"),
            "python": ("Python for Everybody Specialization", "https://www.coursera.org/specializations/python", 35, "beginner"),
        }
        
        if skill in courses:
            title, url, hours, difficulty = courses[skill]
            resources.append(LearningResource(
                title=title,
                type="course",
                url=url,
                estimated_hours=hours,
                difficulty=difficulty,
                relevance_score=gap.importance * gap.confidence,
                skills_covered=[gap.skill]
            ))
        
        # Add article/video
        resources.append(LearningResource(
            title=f"Complete Guide to {gap.skill}",
            type="article",
            url=f"https://medium.com/topic/{skill.replace(' ', '-')}",
            estimated_hours=2,
            difficulty="intermediate",
            relevance_score=gap.importance * gap.confidence * 0.9,
            skills_covered=[gap.skill]
        ))
    
    return sorted(resources, key=lambda x: x.relevance_score, reverse=True)[:15]


def generate_schedule(resources):
    """Generate realistic schedule"""
    
    schedule = []
    current_date = datetime.now()
    
    for i, resource in enumerate(resources[:12]):
        day_offset = i
        schedule_date = current_date + timedelta(days=day_offset)
        
        # Skip weekends
        while schedule_date.weekday() >= 5:
            day_offset += 1
            schedule_date = current_date + timedelta(days=day_offset)
        
        # Vary times
        hours = [7, 19, 20, 7, 19, 20, 7, 19, 20, 7, 19, 20]
        session_time = schedule_date.replace(hour=hours[i], minute=0, second=0, microsecond=0)
        
        schedule.append(LearningSession(
            resource=resource,
            scheduled_time=session_time,
            duration_minutes=30,
            skill_target=resource.skills_covered[0] if resource.skills_covered else "General"
        ))
    
    return schedule
    """Generate a complete demo analysis without API calls"""
    
    # Demo job postings
    jobs = [
        JobPosting(
            title="Senior Machine Learning Engineer",
            company="TechCorp",
            required_skills=["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "SQL", "Docker", "Kubernetes"],
            preferred_skills=["MLOps", "AWS", "Spark"],
            description="Build and deploy ML models at scale. Work with cutting-edge AI technology.",
            url="https://example.com/jobs/techcorp"
        ),
        JobPosting(
            title="ML Engineer",
            company="DataCo",
            required_skills=["Python", "Scikit-learn", "Machine Learning", "Statistics", "Data Analysis", "Git", "Linux"],
            preferred_skills=["NLP", "Computer Vision", "Azure"],
            description="Develop ML solutions for business problems. Strong statistical background required.",
            url="https://example.com/jobs/dataco"
        ),
        JobPosting(
            title="AI/ML Engineer",
            company="StartupXYZ",
            required_skills=["Python", "Machine Learning", "Deep Learning", "PyTorch", "MLOps", "CI/CD", "Docker"],
            preferred_skills=["Kubernetes", "FastAPI", "PostgreSQL"],
            description="Join our AI team building next-gen products. Fast-paced startup environment.",
            url="https://example.com/jobs/startupxyz"
        ),
        JobPosting(
            title="Machine Learning Scientist",
            company="ResearchLabs",
            required_skills=["Python", "Machine Learning", "Deep Learning", "Research", "Mathematics", "Statistics", "PyTorch"],
            preferred_skills=["Publications", "PhD", "NLP"],
            description="Research and develop novel ML algorithms. Academic background preferred.",
            url="https://example.com/jobs/researchlabs"
        ),
        JobPosting(
            title="Senior ML Engineer",
            company="BigTech Inc",
            required_skills=["Python", "TensorFlow", "Machine Learning", "System Design", "Distributed Systems", "Kubernetes", "AWS"],
            preferred_skills=["Scala", "Spark", "Airflow"],
            description="Scale ML systems to millions of users. Strong engineering skills required.",
            url="https://example.com/jobs/bigtech"
        ),
    ]
    
    # Demo skill gaps
    gaps = [
        SkillGap(
            skill="Machine Learning",
            importance=1.0,
            frequency_in_jobs=5,
            confidence=0.95,
            reasoning="Essential for ML Engineer role - appears in all job postings as core requirement"
        ),
        SkillGap(
            skill="Deep Learning",
            importance=0.8,
            frequency_in_jobs=4,
            confidence=0.90,
            reasoning="Critical for modern ML roles - required for neural network development"
        ),
        SkillGap(
            skill="PyTorch",
            importance=0.8,
            frequency_in_jobs=4,
            confidence=0.85,
            reasoning="Industry-standard deep learning framework - highly valued by employers"
        ),
        SkillGap(
            skill="TensorFlow",
            importance=0.6,
            frequency_in_jobs=3,
            confidence=0.85,
            reasoning="Alternative to PyTorch - knowing both frameworks increases opportunities"
        ),
        SkillGap(
            skill="MLOps",
            importance=0.6,
            frequency_in_jobs=3,
            confidence=0.80,
            reasoning="Production ML deployment skills - bridges gap between development and operations"
        ),
        SkillGap(
            skill="Docker",
            importance=0.6,
            frequency_in_jobs=3,
            confidence=0.75,
            reasoning="Containerization is standard for ML deployment - essential DevOps skill"
        ),
        SkillGap(
            skill="Kubernetes",
            importance=0.6,
            frequency_in_jobs=3,
            confidence=0.70,
            reasoning="Container orchestration for scaling ML systems - advanced but valuable"
        ),
        SkillGap(
            skill="Statistics",
            importance=0.4,
            frequency_in_jobs=2,
            confidence=0.85,
            reasoning="Mathematical foundation for ML - important for understanding algorithms"
        ),
        SkillGap(
            skill="AWS",
            importance=0.4,
            frequency_in_jobs=2,
            confidence=0.75,
            reasoning="Cloud platform skills - many companies deploy ML on AWS"
        ),
        SkillGap(
            skill="System Design",
            importance=0.2,
            frequency_in_jobs=1,
            confidence=0.70,
            reasoning="Senior-level skill for architecting scalable ML systems"
        ),
    ]
    
    # Demo learning resources
    resources = [
        LearningResource(
            title="Machine Learning Specialization by Andrew Ng",
            type="course",
            url="https://www.coursera.org/specializations/machine-learning-introduction",
            estimated_hours=60,
            difficulty="beginner",
            relevance_score=0.95,
            skills_covered=["Machine Learning", "Python", "Statistics"]
        ),
        LearningResource(
            title="Deep Learning Specialization",
            type="course",
            url="https://www.coursera.org/specializations/deep-learning",
            estimated_hours=80,
            difficulty="intermediate",
            relevance_score=0.90,
            skills_covered=["Deep Learning", "TensorFlow", "Neural Networks"]
        ),
        LearningResource(
            title="PyTorch for Deep Learning",
            type="course",
            url="https://www.udemy.com/course/pytorch-for-deep-learning/",
            estimated_hours=40,
            difficulty="intermediate",
            relevance_score=0.85,
            skills_covered=["PyTorch", "Deep Learning"]
        ),
        LearningResource(
            title="Full Stack Deep Learning",
            type="course",
            url="https://fullstackdeeplearning.com/",
            estimated_hours=30,
            difficulty="advanced",
            relevance_score=0.85,
            skills_covered=["MLOps", "Deep Learning", "Production ML"]
        ),
        LearningResource(
            title="Docker for Data Science",
            type="course",
            url="https://www.datacamp.com/courses/docker-for-data-science",
            estimated_hours=4,
            difficulty="beginner",
            relevance_score=0.75,
            skills_covered=["Docker", "Containerization"]
        ),
        LearningResource(
            title="Kubernetes for ML Engineers",
            type="article",
            url="https://kubernetes.io/docs/tutorials/",
            estimated_hours=10,
            difficulty="intermediate",
            relevance_score=0.70,
            skills_covered=["Kubernetes", "MLOps"]
        ),
        LearningResource(
            title="Hands-On Machine Learning with Scikit-Learn and TensorFlow",
            type="course",
            url="https://www.oreilly.com/library/view/hands-on-machine-learning/9781492032632/",
            estimated_hours=50,
            difficulty="intermediate",
            relevance_score=0.88,
            skills_covered=["Machine Learning", "TensorFlow", "Python"]
        ),
        LearningResource(
            title="AWS Machine Learning Specialty Certification",
            type="course",
            url="https://aws.amazon.com/certification/certified-machine-learning-specialty/",
            estimated_hours=40,
            difficulty="advanced",
            relevance_score=0.75,
            skills_covered=["AWS", "MLOps", "Cloud Computing"]
        ),
        LearningResource(
            title="Statistical Learning with Python",
            type="course",
            url="https://www.edx.org/course/statistical-learning",
            estimated_hours=30,
            difficulty="intermediate",
            relevance_score=0.80,
            skills_covered=["Statistics", "Machine Learning", "Python"]
        ),
        LearningResource(
            title="MLOps: Machine Learning Operations",
            type="course",
            url="https://www.coursera.org/learn/mlops-fundamentals",
            estimated_hours=20,
            difficulty="intermediate",
            relevance_score=0.82,
            skills_covered=["MLOps", "CI/CD", "Production ML"]
        ),
    ]
    
    # Demo schedule
    schedule = []
    current_date = datetime.now()
    
    for i, resource in enumerate(resources[:10]):
        day_offset = i
        if (current_date + timedelta(days=day_offset)).weekday() >= 5:
            day_offset += 2  # Skip weekends
        
        session_time = current_date + timedelta(days=day_offset)
        session_time = session_time.replace(hour=19, minute=0, second=0, microsecond=0)
        
        schedule.append(LearningSession(
            resource=resource,
            scheduled_time=session_time,
            duration_minutes=30,
            skill_target=resource.skills_covered[0]
        ))
    
    return AnalysisResult(
        profile=profile,
        job_postings=jobs,
        skill_gaps=gaps,
        learning_resources=resources,
        schedule=schedule
    )
