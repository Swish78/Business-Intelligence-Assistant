# Business Intelligence Assistant

A multi-agent system for comprehensive business data analysis using specialized AI agents.

## Overview

This project implements a CrewAI-based system that uses multiple specialized AI agents to analyze business data across different domains:
- Sales analysis
- Marketing optimization
- Customer support evaluation
- Financial health assessment

## Features

- **Multi-Agent System**: Leverages specialized AI agents with domain expertise
- **Comprehensive Analysis**: Examines data across sales, marketing, finance, and support
- **Resilient Design**: Implements retry logic and model switching to handle API limitations
- **Multiple LLM Support**: Configurable to work with various Groq models

## Implementation Details

### Agents

The system includes the following specialized agents:
- **Sales Analyst**: Identifies sales trends and growth opportunities
- **Marketing Strategist**: Analyzes campaign effectiveness and ROI
- **Customer Support Manager**: Evaluates support efficiency
- **Financial Advisor**: Examines financial health and cost optimization

### Technical Notes

I encountered TPM (Tokens Per Minute) limitations while executing the project. I implemented retry logic and model switching, but full execution wasn't possible under the current constraints. Here's my approach:

- **Model Rotation**: The system can switch between multiple Groq models when rate limits are encountered
- **Exponential Backoff**: Implements increasing wait times between retries 
- **Fallback Mechanism**: Gracefully handles API limitations by switching to alternative models
- **Cache Support**: Enables caching to reduce duplicate API calls

## Setup

1. Clone the repository
2. Install requirements
3. Create a `.env` file with the following variables:
   ```
   GROQ_API_KEY=your_groq_api_key
   SERPER_API_KEY=your_serper_api_key
   ```
4. Place your CSV data files in the project directory
5. Run the application

## Usage

The system can be run in two modes:
- **Command Line**: `python crew2.py --no-ui`
- **Gradio Interface**: `python crew2.py`

## License

This project is licensed under the MIT License - see the LICENSE file for details.