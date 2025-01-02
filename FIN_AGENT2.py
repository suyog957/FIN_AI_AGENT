# Import the necessary libraries/modules
from phi.agent import Agent  # The Agent class from the 'phi' library, which is used to create and manage agents
from phi.model.openai import OpenAIChat  # OpenAIChat model, can be used to create a chatbot-style agent using OpenAI's GPT models
from phi.model.groq import Groq  # Groq model, another kind of model used to generate responses or process queries (different from OpenAI)
from phi.tools.duckduckgo import DuckDuckGo  # DuckDuckGo tool for web searches, used to gather information from the web
from phi.tools.yfinance import YFinanceTools  # YFinanceTools is used to fetch financial data, such as stock prices, analyst recommendations, etc.
from dotenv import load_dotenv  # dotenv is used to load environment variables from a .env file (e.g., API keys)

# This loads environment variables from a .env file if available. This is important for securely handling things like API keys.
load_dotenv()

# Here, we create the 'web_agent' which is responsible for gathering information from the web
web_agent = Agent(
    name="Web Agent",  # We name the agent 'Web Agent' to specify its role (web searches)
    model=Groq(id="llama-3.3-70b-versatile"),  # Specify which model the agent uses. In this case, it's Groq's 'llama-3.3-70b-versatile'
    # Alternatively, you could use OpenAI's GPT model by uncommenting the next line:
    # model=OpenAIChat(id="gpt-4o"),
    tools=[DuckDuckGo()],  # The tools the agent will use. Here, the agent uses the DuckDuckGo search tool to fetch data from the web
    instructions=["Always include sources"],  # Instructions for the agent to follow. Here, it should always include the sources of the information it gathers
    show_tool_calls=True,  # This means the agent will print out when it calls a tool (like when it performs a web search)
    markdown=True  # The agent's output will be formatted in markdown, which is useful for displaying results cleanly (e.g., tables, lists)
)

# Now we create the 'finance_agent' which is responsible for financial data, such as stock prices and analyst recommendations
finance_agent = Agent(
    name="Finance Agent",  # The agent is named 'Finance Agent' since it specializes in financial data
    role="Get financial data",  # The agent's role is explicitly defined as 'Get financial data'
    model=Groq(id="llama-3.3-70b-versatile"),  # This agent also uses the 'llama-3.3-70b-versatile' model
    # Alternatively, you could use OpenAI's GPT model by uncommenting the next line:
    # model=OpenAIChat(id="gpt-4o"),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],  # The agent uses YFinanceTools to get stock prices, analyst recommendations, and company info
    instructions=["Use tables to display data"],  # The agent is instructed to use tables to present the data it gathers
    show_tool_calls=True,  # This means the agent will print out when it calls a tool (like when it queries financial data)
    markdown=True  # The agent's output will be formatted in markdown, making it easy to present tables and other structured data
)

# Here we create a team of agents (agent_team), which will include both the 'web_agent' and the 'finance_agent'
agent_team = Agent(
    model=Groq(id="llama-3.3-70b-versatile"),  # The team uses the same 'llama-3.3-70b-versatile' model
    team=[web_agent, finance_agent],  # The team consists of the 'web_agent' and 'finance_agent' that we created earlier
    instructions=["Always include sources", "Use tables to display data"],  # Instructions for the whole team, which should always include sources and present data in tables
    show_tool_calls=True,  # This means the team will print out when any of the agents calls a tool
    markdown=True  # The team’s output will be in markdown format as well
)

# Finally, we ask the agent team to perform a task, which is to summarize analyst recommendations and share the latest news for NVDA (NVIDIA)
agent_team.print_response("Summarize analyst recommendations and share the latest news for NVDA", stream=True)
# 'stream=True' means the response will be printed as it is generated (i.e., in a real-time fashion)
