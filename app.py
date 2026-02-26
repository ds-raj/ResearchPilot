"""
Streamlit frontend for the ArXiv Research Paper Application.
This is the main entry point for the application.
"""

import streamlit as st
import os
import asyncio
import json
import re
import sys
import nest_asyncio
from pipeline import ResearchTeam
from constants import (
    APP_TITLE,
    APP_LAYOUT,
    INITIAL_SIDEBAR_STATE,
    DEFAULT_RESEARCH_TOPICS,
    DEFAULT_MAX_RESULTS,
)
import logging

# Apply nest_asyncio to allow nested event loops (required for Streamlit + asyncio)
nest_asyncio.apply()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configure Streamlit page
st.set_page_config(
    page_title=APP_TITLE,
    layout=APP_LAYOUT,
    initial_sidebar_state=INITIAL_SIDEBAR_STATE,
    menu_items={
        "About": "ArXiv Research Paper Assistant - Powered by AutoGen and OpenAI"
    }
)

# Custom CSS styling
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        color: #2E86C1;
        text-align: center;
    }
    .stMarkdown h2 {
        color: #1F618D;
        margin-top: 2rem;
    }
    .paper-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .paper-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    .paper-authors {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-bottom: 0.5rem;
    }
    .paper-date {
        font-size: 0.85rem;
        opacity: 0.8;
        margin-bottom: 0.8rem;
    }
    .paper-abstract {
        font-size: 0.95rem;
        line-height: 1.4;
        margin-bottom: 0.8rem;
    }
    .paper-link {
        display: inline-block;
        background: white;
        color: #667eea;
        padding: 0.4rem 0.8rem;
        border-radius: 0.4rem;
        text-decoration: none;
        font-weight: bold;
        font-size: 0.9rem;
    }
    .summary-section {
        background: #f0f4ff;
        padding: 1.5rem;
        border-left: 4px solid #667eea;
        border-radius: 0.5rem;
        margin: 2rem 0;
    }
    .metrics {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
        flex-wrap: wrap;
    }
    .metric-box {
        background: #e8eef7;
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        flex: 1;
        min-width: 150px;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #667eea;
    }
    .metric-label {
        font-size: 0.85rem;
        color: #555;
        margin-top: 0.3rem;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_team():
    """Initialize the research team."""
    return ResearchTeam()


def extract_json_from_text(text: str) -> dict:
    """Extract and parse JSON from agent response."""
    try:
        # Try to find JSON array in the text
        json_match = re.search(r'\[\s*\{.*?\}\s*\]', text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    return None


def display_paper_card(paper: dict, index: int):
    """Display a single paper as a styled card."""
    title = paper.get("title", "Unknown Title")
    authors = paper.get("authors", [])
    published = paper.get("published", "Unknown Date")
    abstract = paper.get("abstract", "No abstract available")
    arxiv_url = paper.get("arxiv_url", "")
    
    # Truncate abstract if too long
    abstract_preview = abstract[:300] + "..." if len(abstract) > 300 else abstract
    
    with st.container():
        st.markdown(f"""
        <div class="paper-card">
            <div class="paper-title">📄 {index}. {title}</div>
            <div class="paper-authors">👥 Authors: {', '.join(authors[:3])}{' +' + str(len(authors)-3) + ' more' if len(authors) > 3 else ''}</div>
            <div class="paper-date">📅 Published: {published}</div>
            <div class="paper-abstract">{abstract_preview}</div>
            <a href="{arxiv_url}" target="_blank" class="paper-link">View on arXiv →</a>
        </div>
        """, unsafe_allow_html=True)


def display_papers_section(papers: list):
    """Display all papers in a formatted section."""
    if not papers or not isinstance(papers, list):
        return False
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📚 Total Papers", len(papers))
    with col2:
        st.metric("✍️ Total Authors", sum(len(p.get("authors", [])) for p in papers))
    with col3:
        st.metric("📊 Latest Year", max([int(p.get("published", "2000")[:4]) for p in papers], default=2024))
    
    st.markdown("---")
    st.markdown("### 📚 Research Papers Found")
    
    for idx, paper in enumerate(papers, 1):
        display_paper_card(paper, idx)
    
    return True


def display_summary(summary_text: str):
    """Display the summary in a formatted section."""
    st.markdown("---")
    st.markdown("### 📝 Literature Review Summary")
    
    with st.container():
        st.markdown(f"""
        <div class="summary-section">
        {summary_text}
        </div>
        """, unsafe_allow_html=True)


def render_sidebar():
    """Render the sidebar with configuration options."""
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        st.markdown("---")
        st.subheader("Research Settings")
        
        # Topic selection
        research_mode = st.radio(
            "Select Research Mode:",
            ["Quick Select", "Custom Topic"]
        )
        
        if research_mode == "Quick Select":
            topic = st.selectbox(
                "Choose a research topic:",
                DEFAULT_RESEARCH_TOPICS
            )
        else:
            topic = st.text_input(
                "Enter custom research topic:",
                placeholder="e.g., Quantum Computing, Reinforcement Learning"
            )
        
        # Max results setting
        max_results = st.slider(
            "Maximum papers to retrieve:",
            min_value=1,
            max_value=20,
            value=DEFAULT_MAX_RESULTS,
            step=1
        )
        
        st.markdown("---")
        st.subheader("About")
        st.info(
            "This application uses AutoGen agents to research and summarize "
            "academic papers from arXiv. The system employs two specialized agents: "
            "one for research and one for summarization."
        )
        
        return topic, max_results


def render_main_content(topic: str, max_results: int):
    """Render the main content area."""
    # Header
    st.title("📚 ArXiv Research Paper Assistant")
    st.markdown(
        "Intelligent research and summarization of academic papers using multi-agent collaboration"
    )
    st.markdown("---")
    
    # Display current research topic
    if topic:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.subheader(f"🔍 Researching: {topic}")
        with col2:
            st.metric("Max Results", max_results)
    else:
        st.warning("⚠️ Please select or enter a research topic to begin.")
        return False
    
    return True


async def run_research(topic: str, max_results: int):
    """Execute the research pipeline."""
    team = initialize_team()
    
    # Create tabs for different result views
    tab1, tab2 = st.tabs(["📚 Papers", "📝 Summary"])
    
    with tab1:
        papers_placeholder = st.empty()
    
    with tab2:
        summary_placeholder = st.empty()
    
    papers_data = None
    full_output = ""
    all_messages = []
    
    # Stream results from the research pipeline
    with st.spinner("🔍 Researching papers and generating summary..."):
        async for message in team.run_research(topic):
            if message and hasattr(message, 'content'):
                content = message.content
                all_messages.append(content)
                
                # Try to extract JSON (papers data)
                json_data = extract_json_from_text(content)
                if json_data and papers_data is None:
                    papers_data = json_data
                    with tab1:
                        with papers_placeholder.container():
                            display_papers_section(papers_data)
                
                # Check if it's a summary (doesn't contain JSON)
                if json_data is None and papers_data is not None:
                    full_output += content + "\n"
                    with tab2:
                        with summary_placeholder.container():
                            display_summary(full_output)
    
    # Final display
    if papers_data:
        with tab1:
            st.success("✅ Papers loaded successfully!")
    
    if full_output:
        with tab2:
            st.success("✅ Summary generated successfully!")


def main():
    """Main application entry point."""
    try:
        # Render sidebar and get user inputs
        topic, max_results = render_sidebar()
        
        # Render main content
        can_proceed = render_main_content(topic, max_results)
        
        if not can_proceed:
            return
        
        # Research button
        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            research_button = st.button(
                "🚀 Start Research",
                use_container_width=True,
                type="primary"
            )
        with col2:
            clear_button = st.button(
                "🗑️ Clear Results",
                use_container_width=True
            )
        
        if clear_button:
            st.rerun()
        
        # Execute research when button is clicked
        if research_button:
            try:
                # Run async research function using the event loop
                loop = asyncio.get_event_loop()
                loop.run_until_complete(run_research(topic, max_results))
                
                st.success("✅ Research completed successfully!")
                
            except ValueError as ve:
                st.error(f"⚠️ Configuration Error: {str(ve)}")
                st.info(
                    "Please ensure your `.env` file contains the `OPENAI_API_KEY` variable."
                )
            except Exception as e:
                st.error(f"❌ An error occurred during research: {str(e)}")
                logger.exception("Research execution failed")
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: gray; font-size: 0.8rem;'>"
            "Powered by AutoGen, OpenAI GPT-4o, and arXiv API<br>"
            "© 2026 Research Paper Assistant"
            "</div>",
            unsafe_allow_html=True
        )
        
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        logger.exception("Unexpected error in main")


if __name__ == "__main__":
    main()
