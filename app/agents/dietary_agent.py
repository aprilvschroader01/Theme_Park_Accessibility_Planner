"""
Dietary Agent for Theme Park Accessibility Planner
Uses Azure OpenAI to provide theme park dietary recommendations
"""
import json
import os
from pathlib import Path
from openai import AzureOpenAI
from config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_DEPLOYMENT_NAME,
    AZURE_API_VERSION
)

# Load instructions
INSTRUCTIONS_PATH = Path(__file__).parent / "dietary_agent_instructions.md"
with open(INSTRUCTIONS_PATH, "r") as f:
    SYSTEM_PROMPT = f.read()

class DietaryAgent:
    """Theme park dietary recommendations agent powered by Azure OpenAI"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        self.model = AZURE_DEPLOYMENT_NAME
    
    def generate_plan(self, park_name: str, dietary_restrictions: list, allergens: list) -> dict:
        """
        Generate a dietary plan for the specified theme park
        
        Args:
            park_name: Name of the theme park (e.g., "Magic Kingdom")
            dietary_restrictions: List of dietary restrictions (e.g., ["vegan", "gluten-free"])
            allergens: List of allergens to avoid (e.g., ["peanuts", "shellfish"])
        
        Returns:
            dict with plan_text and structured sections
        """
        
        # Format the user query
        restrictions_text = ", ".join(dietary_restrictions) if dietary_restrictions else "none specified"
        allergens_text = ", ".join(allergens) if allergens else "none specified"
        
        user_message = f"""
Please generate a comprehensive dietary plan for {park_name}.

User Profile:
- Dietary Restrictions: {restrictions_text}
- Allergens to Avoid: {allergens_text}

Follow your pre-planning checklist and provide a complete section-by-section recommendation 
covering all restaurants in each land/section of the park.
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_message.strip()
                    }
                ],
                temperature=0.5,
                max_tokens=4000
            )
            
            plan_text = response.choices[0].message.content
            
            return {
                "success": True,
                "plan": plan_text,
                "park": park_name,
                "dietary_restrictions": dietary_restrictions,
                "allergens": allergens,
                "tokens_used": response.usage.total_tokens
            }
        
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "park": park_name
            }
    
    def parse_sections(self, plan_text: str) -> list:
        """
        Parse the plan text into structured sections
        Returns a list of dictionaries with section info
        """
        sections = []
        current_section = None
        
        lines = plan_text.split("\n")
        
        for line in lines:
            # Detect section headers (e.g., "MAGIC KINGDOM - ADVENTURELAND")
            if line.strip().startswith(("MAGIC KINGDOM", "EPCOT", "HOLLYWOOD", "ANIMAL", "ISLANDS")) and "-" in line:
                if current_section:
                    sections.append(current_section)
                current_section = {
                    "title": line.strip(),
                    "content": []
                }
            elif current_section:
                current_section["content"].append(line)
        
        if current_section:
            sections.append(current_section)
        
        return sections


def create_dietary_agent() -> DietaryAgent:
    """Factory function to create and validate the dietary agent"""
    if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
        raise ValueError(
            "Azure OpenAI credentials not found. "
            "Please set AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT in your .env file"
        )
    return DietaryAgent()
