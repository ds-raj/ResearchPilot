"""
Agent definitions and initialization.
This module contains the setup for all agents used in the research pipeline.
"""

from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from constants import (
    OPENAI_MODEL,
    OPENAI_MODEL2,
    OPENAI_API_KEY_ENV,
    OPENROUTER_BASE_URL,
    ARXIV_RESEARCH_AGENT_NAME,
    SUMMARIZER_AGENT_NAME,
)
from prompts import (
    ARXIV_RESEARCH_AGENT_SYSTEM_MESSAGE,
    SUMMARIZER_AGENT_SYSTEM_MESSAGE,
)

load_dotenv()


def initialize_model_client(model_name: str = OPENAI_MODEL) -> OpenAIChatCompletionClient:
    """
    Initialize and return the OpenRouter model client.
    
    Args:
        model_name (str): The model to use. Defaults to OPENAI_MODEL.
    
    Returns:
        OpenAIChatCompletionClient: Configured OpenRouter client.
        
    Raises:
        ValueError: If API key is not found in environment variables.
    """
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"OPENROUTER_API_KEY not found in environment variables. "
            f"Please set {OPENAI_API_KEY_ENV} in your .env file."
        )
    
    return OpenAIChatCompletionClient(
        base_url=OPENROUTER_BASE_URL,
        model=model_name,
        api_key=api_key,
        model_info={
        "vision": False,
        "function_calling": True,   # ← MUST be True for tools to work
        "json_output": False,
        "family": "unknown",        # use "unknown" for non-OpenAI models
        "structured_output": False,
    })

def create_arxiv_research_agent() -> AssistantAgent:
    """
    Create and configure the ArXiv Research Agent.
    Uses OPENAI_MODEL.
        
    Returns:
        AssistantAgent: Configured ArXiv Research Agent.
    """
    model_client = initialize_model_client(OPENAI_MODEL)
    return AssistantAgent(
        name=ARXIV_RESEARCH_AGENT_NAME,
        description="An agent that researches papers on arXiv.org.",
        model_client=model_client,
        system_message=ARXIV_RESEARCH_AGENT_SYSTEM_MESSAGE,
    )


def create_summarizer_agent() -> AssistantAgent:
    """
    Create and configure the Summarizer Agent.
    Uses OPENAI_MODEL2.
        
    Returns:
        AssistantAgent: Configured Summarizer Agent.
    """
    model_client = initialize_model_client(OPENAI_MODEL2)
    return AssistantAgent(
        name=SUMMARIZER_AGENT_NAME,
        description="An agent that summarizes and synthesizes research papers.",
        model_client=model_client,
        system_message=SUMMARIZER_AGENT_SYSTEM_MESSAGE,
    )