# ArXiv Research Paper Assistant

## 📌 Overview

An intelligent multi-agent application that automates academic research and literature review generation from arXiv papers. Built with AutoGen, OpenAI GPT-4o, and Streamlit.

## 🎯 Features

- **Multi-Agent Collaboration**: Two specialized agents working together (Research + Summarization)
- **Real-time Streaming**: Live output as agents process research
- **Intelligent Search**: Finds most relevant papers using arXiv API
- **Professional Summaries**: Generates formatted literature reviews
- **User-Friendly Interface**: Streamlit-based UI with configuration options
- **Error Handling**: Comprehensive logging and error management

## 🏗️ Project Structure

```
Arxiv_Research_Paper/
├── app.py                  # Main Streamlit application
├── pipeline.py             # Research orchestration
├── agents.py               # Agent initialization
├── constants.py            # Configuration constants
├── prompts.py              # Agent prompts & templates
├── utils.py                # Utility functions
├── requirements.txt        # Project dependencies
├── ARCHITECTURE.md         # Detailed architecture guide
└── .env                    # Environment variables (not in repo)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key

### Installation

1. Clone or download the project
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Usage

1. **Select a Research Topic**:
   - Choose from preset topics or enter a custom topic
   - Adjust maximum number of papers to retrieve

2. **Start Research**:
   - Click the "🚀 Start Research" button
   - Watch real-time results stream in

3. **View Results**:
   - ArXiv Research Agent fetches relevant papers
   - Summarizer Agent creates a literature review
   - Both responses are displayed in markdown format

## 🔧 Configuration

All configuration is centralized in `constants.py`:

- **Model**: GPT-4o (configurable)
- **Max Results**: 5 papers (adjustable via UI)
- **Agent Names**: ArxivResearchAgent, SummarizerAgent
- **Max Turns**: 2 (conversation rounds)

## 📊 Architecture

### Agent Workflow

```
┌─────────────────────────────────────┐
│   User Input (Topic Selection)      │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  ArxivResearchAgent                 │
│  - Formulates search query          │
│  - Fetches top relevant papers      │
│  - Returns JSON paper list          │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│  SummarizerAgent                    │
│  - Analyzes paper list              │
│  - Generates literature review      │
│  - Formats output in Markdown       │
└────────────┬────────────────────────┘
             │
             ▼
┌─────────────────────────────────────┐
│   Display Results (Streamlit UI)    │
└─────────────────────────────────────┘
```

## 🛠️ Core Modules

### app.py
Main Streamlit interface with:
- Sidebar configuration panel
- Topic selection and input
- Real-time result display
- Error handling and user feedback

### pipeline.py
Orchestration layer with:
- `ResearchTeam` class for agent management
- Async research execution
- Stream-based output handling

### agents.py
Agent initialization with:
- OpenAI client setup
- ArXiv Research Agent
- Summarizer Agent
- Environment variable management

### constants.py
Centralized configuration:
- Model settings
- Agent names
- UI configuration
- Default values

### prompts.py
Prompt engineering:
- Research agent system message
- Summarizer agent system message
- Task templates

### utils.py
Utility functions:
- `arxiv_research()`: Search arXiv API
- `format_papers_for_display()`: Format output
- Logging utilities

## 🔐 Environment Variables

Required in `.env`:
- `OPENAI_API_KEY`: Your OpenAI API key

## 📋 Dependencies

- `autogen-agentchat`: Multi-agent orchestration
- `autogen-ext`: AutoGen extensions
- `autogen-ext[openai]`: OpenAI integration
- `streamlit`: Web UI framework
- `arxiv`: arXiv API client
- `python-dotenv`: Environment variable management

See `requirements.txt` for specific versions.

## ⚠️ Important Notes

1. **API Costs**: Running this application will incur OpenAI API costs
2. **Rate Limiting**: Be mindful of arXiv API rate limits
3. **API Key**: Never commit `.env` file to version control
4. **Async Execution**: Application runs async tasks; ensure proper environment setup

## 🐛 Troubleshooting

### "OPENAI_API_KEY not found"
- Ensure `.env` file exists in project root
- Verify the key format is correct
- Check file permissions

### Streamlit Connection Issues
- Ensure all dependencies are installed
- Try running: `pip install -r requirements.txt --upgrade`
- Check if port 8501 is available

### Slow Response Times
- Check internet connection
- Verify OpenAI API status
- Reduce max results for faster processing

## 📈 Performance

- **Typical Research Time**: 30-60 seconds for 5 papers
- **Concurrent Operations**: Supports async processing
- **Memory Usage**: Minimal for normal usage

## 🎓 Learning Resources

- [AutoGen Documentation](https://microsoft.github.io/autogen/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [arXiv API Documentation](https://arxiv.org/help/api)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📝 License

This project is open source. Use and modify as needed.

## 🤝 Contributing

To improve this project:
1. Add tests (currently missing)
2. Implement result caching
3. Add data persistence
4. Improve error recovery
5. Enhance UI/UX

## 📞 Support

For issues or questions:
1. Check the ARCHITECTURE.md file for detailed information
2. Review error logs in the terminal
3. Verify environment setup

## 🌟 Future Enhancements

- [ ] Result caching and persistence
- [ ] User authentication and multi-user support
- [ ] Export research to PDF/Word
- [ ] Integration with reference management tools
- [ ] Advanced filtering and sorting options
- [ ] Custom prompt templates
- [ ] Batch research jobs
