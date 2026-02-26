"""
Team orchestration and research pipeline.
This module manages the multi-agent collaboration for research tasks.
"""

import asyncio
from typing import AsyncGenerator
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent
from agents import create_arxiv_research_agent, create_summarizer_agent
from constants import MAX_TURNS
import logging

logger = logging.getLogger(__name__)


class ResearchTeam:
    """
    Manages the research team and orchestrates agent collaboration.
    """
    
    def __init__(self):
        """Initialize the research team with agents."""
        self.arxiv_agent = create_arxiv_research_agent()
        self.summarizer_agent = create_summarizer_agent()
        self.team = self._create_team()
    
    def _create_team(self) -> RoundRobinGroupChat:
        """
        Create and configure the team for round-robin collaboration.
        
        Returns:
            RoundRobinGroupChat: Configured team for agent collaboration.
        """
        return RoundRobinGroupChat(
            participants=[self.arxiv_agent, self.summarizer_agent],
            max_turns=MAX_TURNS
        )
    
    async def run_research(self, topic: str) -> AsyncGenerator[str, None]:
        """
        Execute the research pipeline for a given topic.
        
        Args:
            topic (str): The research topic to investigate.
            
        Yields:
            str: Messages from the agents during execution.
        """
        # Pass only the topic name to the agents, not the full task template
        logger.info(f"Starting research for topic: {topic}")
        
        try:
            async for msg in self.team.run_stream(task=topic):
                yield msg
            logger.info(f"Completed research for topic: {topic}")
        except Exception as e:
            logger.error(f"Error during research execution: {str(e)}")
            raise


async def run_research_pipeline(topic: str) -> None:
    """
    High-level function to run the research pipeline.
    
    Args:
        topic (str): The research topic to investigate.
    """
    team = ResearchTeam()
    async for message in team.run_research(topic):
        print(message)
        print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    asyncio.run(run_research_pipeline("Agentic AI"))
