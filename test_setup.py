#!/usr/bin/env python3
"""
Test script to verify the Career Growth Agent setup
"""

import os
import sys
from dotenv import load_dotenv


def test_environment():
    """Test environment variables"""
    print("🔍 Testing environment variables...")
    
    load_dotenv()
    
    checks = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPIK_API_KEY": os.getenv("OPIK_API_KEY"),
    }
    
    all_good = True
    for key, value in checks.items():
        if value:
            print(f"  ✓ {key} is set")
        else:
            print(f"  ✗ {key} is NOT set")
            all_good = False
    
    return all_good


def test_imports():
    """Test that all required packages are installed"""
    print("\n📦 Testing package imports...")
    
    packages = [
        ("opik", "opik"),
        ("openai", "openai"),
        ("pydantic", "pydantic"),
        ("dotenv", "python-dotenv"),
        ("bs4", "beautifulsoup4"),
        ("requests", "requests"),
    ]
    
    all_good = True
    for module, package in packages:
        try:
            __import__(module)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ✗ {package} - run: pip install {package}")
            all_good = False
    
    return all_good


def test_agents():
    """Test that agent modules can be imported"""
    print("\n🤖 Testing agent modules...")
    
    modules = [
        "career_agent.models",
        "career_agent.job_analyzer",
        "career_agent.skill_gap_agent",
        "career_agent.resource_curator",
        "career_agent.scheduler_agent",
        "career_agent.orchestrator",
    ]
    
    all_good = True
    for module in modules:
        try:
            __import__(module)
            print(f"  ✓ {module}")
        except Exception as e:
            print(f"  ✗ {module} - {str(e)}")
            all_good = False
    
    return all_good


def test_opik_connection():
    """Test Opik connection"""
    print("\n🔗 Testing Opik connection...")
    
    try:
        import opik
        opik.configure(api_key=os.getenv("OPIK_API_KEY"))
        print("  ✓ Opik configured successfully")
        return True
    except Exception as e:
        print(f"  ⚠️  Opik configuration warning: {str(e)}")
        print("  Note: Demo will work but traces may not be logged")
        return True  # Non-critical


def test_openai_connection():
    """Test OpenAI connection"""
    print("\n🔗 Testing OpenAI connection...")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Simple test call
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        
        if response.choices[0].message.content:
            print("  ✓ OpenAI API working")
            return True
        else:
            print("  ✗ OpenAI API returned empty response")
            return False
            
    except Exception as e:
        print(f"  ✗ OpenAI API error: {str(e)}")
        return False


def main():
    print("="*60)
    print("Career Growth Agent - Setup Test")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Environment", test_environment()))
    results.append(("Imports", test_imports()))
    results.append(("Agents", test_agents()))
    results.append(("Opik", test_opik_connection()))
    results.append(("OpenAI", test_openai_connection()))
    
    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    all_passed = True
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {name}")
        if not passed:
            all_passed = False
    
    print("="*60)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run the demo.")
        print("\nNext steps:")
        print("  1. Run CLI demo: python -m career_agent.main")
        print("  2. Run web UI: streamlit run app.py")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("  - Install packages: pip install -r requirements.txt")
        print("  - Set API keys in .env file (see .env.example)")
        return 1


if __name__ == "__main__":
    sys.exit(main())
