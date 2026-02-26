"""
Constants and configuration for the ArXiv Research Paper Application.
This module centralizes all configuration values used across the application.
"""
from dotenv import load_dotenv
import os

load_dotenv()

# OpenRouter Model Configuration (Free Tier)
# Using DeepSeek R1 - Free and capable model
# Get your free API key from: https://openrouter.ai/keys
OPENAI_MODEL = "nvidia/nemotron-3-nano-30b-a3b:free"
OPENAI_MODEL2 = "nvidia/nemotron-3-nano-30b-a3b:free"
OPENAI_API_KEY_ENV = "OPENROUTER_API_KEY"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# ArXiv Search Configuration
DEFAULT_MAX_RESULTS = 5
ARXIV_SORT_CRITERION = "Relevance"  # Options: Relevance, SubmittedDate, LastUpdatedDate
ARXIV_SORT_ORDER = "Descending"  # Options: Ascending, Descending

# Agent Names
ARXIV_RESEARCH_AGENT_NAME = "ArxivResearchAgent"
SUMMARIZER_AGENT_NAME = "SummarizerAgent"

# Team Configuration
MAX_TURNS = 2

# Streamlit UI Configuration
APP_TITLE = "ArXiv Research Paper Assistant"
APP_LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# Default Research Topics
DEFAULT_RESEARCH_TOPICS = [
    "Agentic AI",
    "Large Language Models",
    "Machine Learning",
    "Deep Learning",
    "Natural Language Processing",
]

# Output Configuration
PAPERS_PER_PAGE = 5