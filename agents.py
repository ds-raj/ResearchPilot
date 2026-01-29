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
    OPENAI_API_KEY_ENV,
    ARXIV_RESEARCH_AGENT_NAME,
    SUMMARIZER_AGENT_NAME,
)
from prompts import (
    ARXIV_RESEARCH_AGENT_SYSTEM_MESSAGE,
    SUMMARIZER_AGENT_SYSTEM_MESSAGE,
)

load_dotenv()


def initialize_model_client() -> OpenAIChatCompletionClient:
    """
    Initialize and return the OpenAI model client.
    
    Returns:
        OpenAIChatCompletionClient: Configured OpenAI client.
        
    Raises:
        ValueError: If API key is not found in environment variables.
    """
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"OPENAI_API_KEY not found in environment variables. "
            f"Please set {OPENAI_API_KEY_ENV} in your .env file."
        )
    
    return OpenAIChatCompletionClient(model=OPENAI_MODEL, api_key=api_key)


def create_arxiv_research_agent(model_client: OpenAIChatCompletionClient) -> AssistantAgent:
    """
    Create and configure the ArXiv Research Agent.
    
    Args:
        model_client (OpenAIChatCompletionClient): The model client for the agent.
        
    Returns:
        AssistantAgent: Configured ArXiv Research Agent.
    """
    return AssistantAgent(
        name=ARXIV_RESEARCH_AGENT_NAME,
        description="An agent that researches papers on arXiv.org.",
        model_client=model_client,
        system_message=ARXIV_RESEARCH_AGENT_SYSTEM_MESSAGE,
        tools=[],
    )


def create_summarizer_agent(model_client: OpenAIChatCompletionClient) -> AssistantAgent:
    """
    Create and configure the Summarizer Agent.
    
    Args:
        model_client (OpenAIChatCompletionClient): The model client for the agent.
        
    Returns:
        AssistantAgent: Configured Summarizer Agent.
    """
    return AssistantAgent(
        name=SUMMARIZER_AGENT_NAME,
        description="An agent that summarizes and synthesizes research papers.",
        model_client=model_client,
        system_message=SUMMARIZER_AGENT_SYSTEM_MESSAGE,
        tools=[],
    )
