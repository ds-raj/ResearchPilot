"""
Utility functions for ArXiv research and data processing.
"""

from typing import List, Dict
import arxiv
import logging

logger = logging.getLogger(__name__)


def arxiv_research(query: str, max_results: int = 5) -> List[Dict]:
    """
    Search arXiv.org for papers matching the query.
    
    Args:
        query (str): The search query for arXiv papers.
        max_results (int): Maximum number of results to return. Default is 5.
    
    Returns:
        List[Dict]: A list of paper dictionaries containing:
            - title: Paper title
            - authors: List of author names
            - abstract: Paper summary
            - arxiv_url: URL to the paper
            - published: Publication date in YYYY-MM-DD format
            
    Raises:
        Exception: If the arXiv API request fails.
    """
    try:
        client = arxiv.Client()
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
            sort_order=arxiv.SortOrder.Descending,
        )
        
        papers: List[Dict] = []
        for result in client.results(search):
            paper = {
                "title": result.title,
                "authors": [author.name for author in result.authors],
                "abstract": result.summary,
                "arxiv_url": result.entry_id,
                "published": result.published.strftime("%Y-%m-%d"),
            }
            papers.append(paper)
        
        logger.info(f"Successfully fetched {len(papers)} papers for query: {query}")
        return papers
        
    except Exception as e:
        logger.error(f"Error fetching papers from arXiv: {str(e)}")
        raise


def format_papers_for_display(papers: List[Dict]) -> str:
    """
    Format papers list into a readable string format.
    
    Args:
        papers (List[Dict]): List of paper dictionaries.
        
    Returns:
        str: Formatted string representation of papers.
    """
    formatted = "📚 Research Papers Found:\n\n"
    for idx, paper in enumerate(papers, 1):
        formatted += f"{idx}. **{paper['title']}**\n"
        formatted += f"   Authors: {', '.join(paper['authors'][:3])}"
        if len(paper['authors']) > 3:
            formatted += f", +{len(paper['authors']) - 3} more"
        formatted += f"\n   Published: {paper['published']}\n"
        formatted += f"   URL: {paper['arxiv_url']}\n\n"
    return formatted
