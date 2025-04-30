#!/usr/bin/env python3
# coding: utf-8

"""
L4: Tools for Customer Outreach Campaign with OpenAI
"""

from crewai import Agent, Task, Crew
from crewai.tools import BaseTool  
from crewai_tools import DirectoryReadTool, FileReadTool, SerperDevTool 
import os
from dotenv import load_dotenv
import warnings

warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Configure OpenAI
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
os.environ["OPENAI_MODEL_NAME"] = 'gpt-4-turbo'

# --- AGENTS ---
sales_rep_agent = Agent(
    role="Sales Representative",
    goal="Identify high-value leads matching ideal customer profile",
    backstory=(
        "As part of CrewAI's sales team, you scour digital landscapes "
        "for potential leads using cutting-edge tools and strategic analysis."
    ),
    allow_delegation=False,
    verbose=True
)

lead_sales_rep_agent = Agent(
    role="Lead Sales Representative",
    goal="Nurture leads with personalized communications",
    backstory=(
        "Bridge between potential clients and solutions at CrewAI, "
        "creating engaging messages that convert interest into action."
    ),
    allow_delegation=False,
    verbose=True
)

# --- TOOLS ---
directory_read_tool = DirectoryReadTool(directory='./instructions')
file_read_tool = FileReadTool()
search_tool = SerperDevTool(serper_api_key=SERPER_API_KEY)

class SentimentAnalysisTool(BaseTool):
    name: str = "Sentiment Analysis Tool"
    description: str = "Analyzes text sentiment for positive communication"
    
    def _run(self, text: str) -> str:
        # Your custom code tool goes here
        return "positive"

sentiment_analysis_tool = SentimentAnalysisTool()

# --- TASKS ---
lead_profiling_task = Task(
    description=(
        "Analyze {lead_name} in {industry} sector using all available data "
        "to create detailed profile with decision-makers and needs."
    ),
    expected_output=(
        "Comprehensive report on {lead_name} including background, "
        "key personnel, and engagement strategies."
    ),
    tools=[directory_read_tool, file_read_tool, search_tool],
    agent=sales_rep_agent,
)

personalized_outreach_task = Task(
    description=(
        "Create personalized outreach for {lead_name} targeting "
        "{key_decision_maker} regarding {milestone}."
    ),
    expected_output=(
        "Series of professional email drafts aligned with "
        "{lead_name}'s corporate identity."
    ),
    tools=[sentiment_analysis_tool, search_tool],
    agent=lead_sales_rep_agent,
)

# --- CREW ---
crew = Crew(
    agents=[sales_rep_agent, lead_sales_rep_agent],
    tasks=[lead_profiling_task, personalized_outreach_task],
    verbose=True,
    memory=True  # Safe to enable with OpenAI
)

# --- EXECUTION ---
if __name__ == "__main__":
    inputs = {
        "lead_name": "DeepLearningAI",
        "industry": "Online Learning Platform",
        "key_decision_maker": "Andrew Ng",
        "position": "CEO",
        "milestone": "product launch"
    }

    result = crew.kickoff(inputs=inputs)
    print("\n=== Final Response ===\n")
    print(result)