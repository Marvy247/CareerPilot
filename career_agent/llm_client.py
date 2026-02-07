"""Unified LLM client that supports multiple providers including free ones"""

import os
import json
from typing import Optional


class LLMClient:
    """Unified client for multiple LLM providers"""
    
    def __init__(self):
        self.provider = self._detect_provider()
        self.client = self._initialize_client()
    
    def _detect_provider(self) -> str:
        """Detect which LLM provider to use based on available API keys"""
        if os.getenv("GROQ_API_KEY"):
            return "groq"
        elif os.getenv("GOOGLE_API_KEY"):
            return "google"
        elif os.getenv("OPENAI_API_KEY"):
            return "openai"
        elif os.getenv("ANTHROPIC_API_KEY"):
            return "anthropic"
        else:
            return "none"
    
    def _initialize_client(self):
        """Initialize the appropriate client"""
        if self.provider == "groq":
            from groq import Groq
            return Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        elif self.provider == "google":
            import google.generativeai as genai
            genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
            return genai.GenerativeModel('models/gemini-flash-latest')
        
        elif self.provider == "openai":
            from openai import OpenAI
            try:
                from opik.integrations.openai import track_openai
                return track_openai(OpenAI(api_key=os.getenv("OPENAI_API_KEY")))
            except:
                return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        elif self.provider == "anthropic":
            from anthropic import Anthropic
            return Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        return None
    
    def generate(self, system_prompt: str, user_prompt: str, temperature: float = 0.7) -> str:
        """Generate text using the configured provider"""
        
        if self.provider == "groq":
            # Groq (free and fast!)
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Free tier model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        
        elif self.provider == "google":
            # Google Gemini
            full_prompt = f"{system_prompt}\n\n{user_prompt}"
            response = self.client.generate_content(
                full_prompt,
                generation_config={"temperature": temperature}
            )
            return response.text
        
        elif self.provider == "openai":
            # OpenAI
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=temperature
            )
            return response.choices[0].message.content
        
        elif self.provider == "anthropic":
            # Anthropic Claude
            response = self.client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                system=system_prompt,
                messages=[{"role": "user", "content": user_prompt}],
                temperature=temperature
            )
            return response.content[0].text
        
        else:
            raise ValueError("No LLM provider configured. Please set GOOGLE_API_KEY, OPENAI_API_KEY, or ANTHROPIC_API_KEY")
    
    def generate_json(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> dict:
        """Generate JSON response"""
        response = self.generate(system_prompt, user_prompt, temperature)
        
        # Try to extract JSON from response
        try:
            # Sometimes LLMs wrap JSON in markdown code blocks
            if "```json" in response:
                response = response.split("```json")[1].split("```")[0].strip()
            elif "```" in response:
                response = response.split("```")[1].split("```")[0].strip()
            
            return json.loads(response)
        except:
            # If parsing fails, try to find JSON in the text
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise ValueError(f"Could not parse JSON from response: {response}")
