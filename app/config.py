"""
Configuration for Theme Park Accessibility Planner
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_DEPLOYMENT_NAME = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-35-turbo")
AZURE_API_VERSION = os.getenv("AZURE_API_VERSION", "2024-02-01")

# Flask Configuration
FLASK_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = FLASK_ENV == "development"

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/app.db")

# Create data directory if it doesn't exist
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
