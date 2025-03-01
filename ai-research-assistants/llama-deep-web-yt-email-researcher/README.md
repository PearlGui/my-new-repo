# Llama Deep Web + YouTube Email Researcher (Task 2)

## Overview
This folder contains the code for **Task 2** of the assignment. The script can:
1. Search YouTube for videos on a given topic (using the YouTube Data API).
2. (Optionally) summarize those videos using an LLM (e.g., OpenAI, Ollama).
3. Send the results via email.

## Installation
1. **Python**: Ensure Python 3.8+ is installed.
2. **Create a virtual environment** (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   
pip install langchain openai google-api-python-client
export YOUTUBE_API_KEY="your-youtube-api-key"

