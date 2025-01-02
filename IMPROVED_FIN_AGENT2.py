# Import necessary libraries
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Function to create a web agent
def create_web_agent(model: str = "llama-3.3-70b-versatile"):
    return Agent(
        name="Web Agent",
        model=Groq(id=model),  # You can change the model here if needed
        tools=[DuckDuckGo()],  # DuckDuckGo for web searches
        instructions=["Always include sources", "Fetch related news if available"],
        show_tool_calls=True,
        markdown=True
    )

# Function to create a finance agent
def create_finance_agent(model: str = "llama-3.3-70b-versatile"):
    return Agent(
        name="Finance Agent",
        role="Get financial data",
        model=Groq(id=model),  # Same for finance agent, Groq or OpenAI models can be used
        tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
        instructions=["Use tables to display data", "Include stock-related news if available"],
        show_tool_calls=True,
        markdown=True
    )

# Function to create a team of agents
def create_agent_team(web_agent, finance_agent, model: str = "llama-3.3-70b-versatile"):
    return Agent(
        model=Groq(id=model),  # We specify the model for the whole team
        team=[web_agent, finance_agent],
        instructions=["Always include sources", "Use tables to display data", "Provide a comprehensive summary"],
        show_tool_calls=True,
        markdown=True
    )

# Function to summarize recommendations and fetch latest news for a given company or stock symbol
def get_summary_and_news(agent_team, company_symbol: str):
    prompt = f"Summarize analyst recommendations and share the latest news for {company_symbol}"
    # Streaming the response for real-time updates
    agent_team.print_response(prompt, stream=True)

# Main entry point of the program
if __name__ == "__main__":
    # Create agents
    web_agent = create_web_agent()
    finance_agent = create_finance_agent()

    # Create an agent team
    agent_team = create_agent_team(web_agent, finance_agent)

    # Task: Get summary and latest news for NVDA (NVIDIA)
    get_summary_and_news(agent_team, "NVDA")
