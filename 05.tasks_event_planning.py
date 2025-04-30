#!/usr/bin/env python3
# coding: utf-8

"""
L5: Automate Event Planning (VS Code version)
"""

import warnings
import os
import json
from pprint import pprint
from crewai import Agent, Crew, Task
from crewai_tools import ScrapeWebsiteTool, SerperDevTool
from pydantic import BaseModel

warnings.filterwarnings('ignore')

# If you have utility functions for API keys, import and use them here.
try:
    from utils import get_openai_api_key, get_serper_api_key
    openai_api_key = get_openai_api_key()
    serper_api_key = get_serper_api_key()
except ImportError:
    openai_api_key = os.getenv("OPENAI_API_KEY")
    serper_api_key = os.getenv("SERPER_API_KEY")

# Set environment variables for CrewAI and tools
os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'
if serper_api_key:
    os.environ["SERPER_API_KEY"] = serper_api_key

# --- Initialize tools ---
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()

# --- Creating Agents ---
venue_coordinator = Agent(
    role="Venue Coordinator",
    goal="Identify and book an appropriate venue based on event requirements",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "With a keen sense of space and understanding of event logistics, "
        "you excel at finding and securing the perfect venue that fits the event's theme, "
        "size, and budget constraints."
    )
)

logistics_manager = Agent(
    role='Logistics Manager',
    goal=(
        "Manage all logistics for the event including catering and equipmen"
    ),
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Organized and detail-oriented, you ensure that every logistical aspect of the event "
        "from catering to equipment setup is flawlessly executed to create a seamless experience."
    )
)

marketing_communications_agent = Agent(
    role="Marketing and Communications Agent",
    goal="Effectively market the event and communicate with participants",
    tools=[search_tool, scrape_tool],
    verbose=True,
    backstory=(
        "Creative and communicative, you craft compelling messages and "
        "engage with potential attendees to maximize event exposure and participation."
    )
)

# --- VenueDetails Pydantic Model ---
class VenueDetails(BaseModel):
    name: str
    address: str
    capacity: int
    booking_status: str

# --- Creating Tasks ---
venue_task = Task(
    description="Find a venue in {event_city} that meets criteria for {event_topic}.",
    expected_output="All the details of a specifically chosen venue you found to accommodate the event.",
    human_input=True,
    output_json=VenueDetails,
    output_file="venue_details.json",
    agent=venue_coordinator
)

logistics_task = Task(
    description="Coordinate catering and equipment for an event with {expected_participants} participants on {tentative_date}.",
    expected_output="Confirmation of all logistics arrangements including catering and equipment setup.",
    human_input=True,
    async_execution=False,
    agent=logistics_manager
)

marketing_task = Task(
    description="Promote the {event_topic} aiming to engage at least {expected_participants} potential attendees.",
    expected_output="Report on marketing activities and attendee engagement formatted as markdown.",
    async_execution=True,
    output_file="marketing_report.md",
    agent=marketing_communications_agent
)

# --- Crew Setup ---
event_management_crew = Crew(
    agents=[venue_coordinator, logistics_manager, marketing_communications_agent],
    tasks=[venue_task, logistics_task, marketing_task],
    verbose=True
)

# --- Running the Crew ---
if __name__ == "__main__":
    event_details = {
        'event_topic': "Tech Innovation Conference",
        'event_description': "A gathering of tech innovators and industry leaders to explore future technologies.",
        'event_city': "San Francisco",
        'tentative_date': "2024-09-15",
        'expected_participants': 500,
        'budget': 20000,
        'venue_type': "Conference Hall"
    }

    result = event_management_crew.kickoff(inputs=event_details)
    print("\n=== CrewAI Output ===\n")
    print(result)

    # Display the generated venue_details.json file
    try:
        with open('venue_details.json') as f:
            data = json.load(f)
            print("\n=== Venue Details ===")
            pprint(data)
    except FileNotFoundError:
        print("venue_details.json not found. Wait a moment and try again.")

    # Display the generated marketing_report.md file
    try:
        with open('marketing_report.md') as f:
            print("\n=== Marketing Report ===")
            print(f.read())
    except FileNotFoundError:
        print("marketing_report.md not found. Wait a moment and try again.")
