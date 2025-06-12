from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # Groq Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = "llama-3.3-70b-versatile"  # or "llama2-70b-4096" or other Groq supported models
    
    # TMDB Configuration
    TMDB_API_KEY: str = os.getenv("TMDB_API_KEY", "")
    TMDB_API_BASE_URL: str = "https://api.themoviedb.org/3"
    
    # Database Configuration
    DATABASE_URL: str = "sqlite:///./movie_agent.db"
    
    # Agent Configuration
    MAX_CONVERSATION_TURNS: int = 10
    TEMPERATURE: float = 0.7
    MAX_TOKENS: int = 1000
    
    # System Messages
    SYSTEM_MESSAGE: str = """You are a helpful movie recommendation assistant. 
    Your goal is to understand user preferences and provide personalized movie recommendations.
    Be conversational, ask clarifying questions when needed, and maintain context throughout the conversation."""
    
    class Config:
        env_file = ".env"

settings = Settings() 