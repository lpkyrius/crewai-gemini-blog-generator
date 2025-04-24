import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
import warnings

warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Set up Gemini LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",  # or "gemini-pro"
    verbose=True,
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)

# For Open AI API you can use:
# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# os.environ["OPENAI_MODEL_NAME"] = 'gpt-3.5-turbo'

# Define agents with Gemini LLM
planner = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content on {topic}",
    backstory=(
        "You're working on planning a blog article about the topic: {topic}. "
        "You collect information to help the audience learn and make informed decisions. "
        "Your work is the basis for the Content Writer."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate opinion piece about the topic: {topic}",
    backstory=(
        "You're writing a new opinion piece about the topic: {topic}. "
        "You base your writing on the work of the Content Planner, who provides an outline and context. "
        "You follow the outline and provide objective, impartial insights."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with the writing style of the organization.",
    backstory=(
        "You are an editor who receives a blog post from the Content Writer. "
        "You review the post for journalistic best practices and balanced viewpoints."
    ),
    allow_delegation=False,
    verbose=True,
    llm=llm
)

# Define tasks
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering their interests and pain points.\n"
        "3. Develop a detailed content outline including an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output=(
        "A comprehensive content plan document with an outline, audience analysis, SEO keywords, and resources."
    ),
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
        "3. Sections/Subtitles are properly named in an engaging manner.\n"
        "4. Ensure the post is structured with an engaging introduction, insightful body, and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and alignment with the brand's voice.\n"
    ),
    expected_output=(
        "A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs."
    ),
    agent=writer,
)

edit = Task(
    description=(
        "Proofread the given blog post for grammatical errors and alignment with the brand's voice."
    ),
    expected_output=(
        "A well-written blog post in markdown format, ready for publication, each section should have 2 or 3 paragraphs."
    ),
    agent=editor
)

# Assemble Crew
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2
)

if __name__ == "__main__":
    topic = "Artificial Intelligence"  # Change the topic as needed
    result = crew.kickoff(inputs={"topic": topic})
    print(result)
