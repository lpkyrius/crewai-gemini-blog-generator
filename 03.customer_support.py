#!/usr/bin/env python3
# coding: utf-8

"""
L3: Multi-agent Customer Support Automation

Demonstrates:
- Role Playing
- Focus
- Tools
- Cooperation
- Guardrails
- Memory
"""
# Load environment variables
import os
import lzma
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from crewai_tools import (
    SerperDevTool, # search using Google Search
    ScrapeWebsiteTool, # simple scraping tool (extracting content from a url)
    WebsiteSearchTool  # does RAG over a website, semantic search 
    )
# from utils import get_openai_api_key  # Ensure this exists or replace with your method
import warnings
warnings.filterwarnings('ignore')

# Set up Gemini LLM
# llm = ChatGoogleGenerativeAI(
#     model="gemini-1.5-flash",  # or "gemini-pro"
#     verbose=True,
#     temperature=0.5,
#     google_api_key=GOOGLE_API_KEY
# )

# Here we must use the Open AI API for the following reasons:
# - CrewAI uses OpenAI embeddings by default when memory=True (for agent memory and RAG features).
# - When you enable memory=True in your Crew definition, CrewAI tries to use OpenAI for embeddings, even if your main LLM is Gemini.

# Set up OpenAI API key and model (if using OpenAI)
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# ## Role Playing, Focus and Cooperation

# --- AGENTS ---

support_agent = Agent(
    role="Senior Support Representative",
	goal="Be the most friendly and helpful "
        "support representative in your team",
	backstory=(
		"You work at crewAI (https://crewai.com) and "
        " are now working on providing "
		"support to {customer}, a super important customer "
        " for your company."
		"You need to make sure that you provide the best support!"
		"Make sure to provide full complete answers, "
        " and make no assumptions."
	),
	allow_delegation=False,
	verbose=True
)

# - By not setting `allow_delegation=False`, `allow_delegation` takes its default value of being `True`.
# - This means the agent _can_ delegate its work to another agent which is better suited to do a particular task. 

support_quality_assurance_agent = Agent(
	role="Support Quality Assurance Specialist",
	goal="Get recognition for providing the "
    "best support quality assurance in your team",
	backstory=(
		"You work at crewAI (https://crewai.com) and "
        "are now working with your team "
		"on a request from {customer} ensuring that "
        "the support representative is "
		"providing the best support possible.\n"
		"You need to make sure that the support representative "
        "is providing full"
		"complete answers, and make no assumptions."
	),
	verbose=True
)

# * **Role Playing**: Both agents have been given a role, goal and backstory.
# * **Focus**: Both agents have been prompted to get into the character of the roles they are playing.
# * **Cooperation**: Support Quality Assurance Agent can delegate work back to the Support Agent, allowing for these agents to work together.

# --- TOOLS ---
# ### Possible Custom Tools
# - Load customer data
# - Tap into previous conversations
# - Load data from a CRM
# - Checking existing bug reports
# - Checking existing feature requests
# - Checking ongoing tickets
# - ... and more

# - Some ways of using CrewAI tools.
# 
# ```Python
# search_tool = SerperDevTool()
# scrape_tool = ScrapeWebsiteTool()
# ```

# - Instantiate a document scraper tool.
# - The tool will scrape a page (only 1 URL) of the CrewAI documentation.

# Let's avoid the agent scrap any url by point a specific one using website_url=
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
)


# ##### Different Ways to Give Agents Tools
# 
# - Agent Level: The Agent can use the Tool(s) on any Task it performs.
# - Task Level: The Agent will only use the Tool(s) when performing that specific Task.
# 
# **Note**: Task Tools override the Agent Tools.

# ### Creating Tasks
# - You are passing the Tool on the Task Level.

# Tasks tools override the Agent tools.

# --- TASKS ---

inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
	    "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
		"Make sure to use everything you know "
        "to provide the best support possible."
		"You must strive to provide a complete "
        "and accurate response to the customer's inquiry."
    ),
    expected_output=(
	    "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
		"leaving no questions unanswered, and maintain a helpful and friendly "
		"tone throughout."
    ),
	tools=[docs_scrape_tool],
    agent=support_agent,
)

# - `quality_assurance_review` is not using any Tool(s)
# - Here the QA Agent will only review the work of the Support Agent

quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
		"high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
		"thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
		"ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
		"relevant feedback and improvements.\n"
		"Don't be too formal, we are a chill and cool company "
	    "but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent,
)

# --- CREW ---

crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    verbose=True,
    memory=True # Enable memory to store and recall information across tasks: short, long and entity memory.
)

# --- RUN WORKFLOW ---

if __name__ == "__main__":
    inputs = {
        "customer": "DeepLearningAI",
        "person": "Mathew Peters",
        "inquiry": (
            "I need help with setting up a Crew and kicking it off, specifically "
            "how can I add memory to my crew? Can you provide guidance?"
        )
    }
    result = crew.kickoff(inputs=inputs)
    print("\n=== Final Response ===\n")
    print(result)
    print("\n=== The End ===\n")