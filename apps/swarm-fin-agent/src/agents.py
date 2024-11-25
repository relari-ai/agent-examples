from swarm import Swarm, Agent
from tools import (
    get_stock_price,
    get_company_profile,
    get_financial_ratios,
    get_key_metrics,
    get_market_cap,
    get_stock_screener,
    generate_single_line_item_query,
    read_webpage
)

def transfer_to_summarizer():
    print("Transferring to summarizer")
    return summarizing_agent

def transfer_to_web_researcher():
    print("Transferring to web researcher")
    return web_researcher_agent

def transfer_to_financial_data_agent():
    print("Transferring to financial data agent")
    return financial_data_agent

def transfer_to_supervisor():
    print("Transferring to supervisor")
    return supervisor_agent

# Financial Data Agent
financial_data_agent = Agent(
    name="Financial Data Agent",
    instructions="""You are a financial data specialist responsible for retrieving financial data using the provided API tools.
    Your tasks:
    1. Given a user query, use the appropriate tool to fetch relevant financial data
    2. Return only the raw data obtained from the tool
    3. Do not add commentary or explanations
    4. Focus on gathering accurate and up-to-date information
    5. Once you have gathered the relevant financial data, you can transfer the task back to the Supervisor Agent for further processing.
    
    Always provide unprocessed data as your response.""",
    functions=[
        get_stock_price,
        get_company_profile,
        get_financial_ratios,
        get_key_metrics,
        get_market_cap,
        get_stock_screener,
        generate_single_line_item_query,
        transfer_to_supervisor,
    ]
)


# Web Researcher Agent
web_researcher_agent = Agent(
    name="Web Researcher Agent",
    instructions="""You are a web researcher responsible for gathering information from the web.
    Your tasks:
    1. Given a user query, use the appropriate tool to fetch relevant information from the web
    2. Return only the raw data obtained from the tool
    3. Do not add commentary or explanations
    4. Focus on gathering accurate and up-to-date information
    5. Once you have gathered the relevant information, you can transfer the task back to the Supervisor Agent for further processing.
    """,
    functions=[
        read_webpage,
        transfer_to_supervisor,
    ]
)

# Summarizing Agent
summarizing_agent = Agent(
    name="Financial Analysis Reporter",
    instructions="""You are a skilled financial analyst responsible for synthesizing information.
    Your tasks:
    1. Analyze data provided by the Supervisor Agent who has gathered data from Financial Data Agent, and Web Researcher Agent
    2. Create clear, concise summaries of financial findings
    3. Present information in a user-friendly format
    4. Use tables when appropriate to improve readability
    
    Focus on providing actionable insights and clear explanations."""
)

# Supervisor Agent
supervisor_agent = Agent(
    name="Supervisor",
    instructions="""You are a supervisor agent responsible for coordinating the Financial Data Agent, Web Researcher Agent, and Summarizing Agent.
    Your tasks:
    1. Given a user query, determine which agent to delegate the task to based on the user's query
    2. If the user's query requires financial data, delegate to the Financial Data Agent
    3. If the user's query requires web research, delegate to the Web Researcher Agent
    4. If there's enough information already available to answer the user's query, delegate to the Summarizing Agent for final output. 
    Never summarize the data yourself. Always delegate to the Summarizing Agent to provide the final output.
    """,
    functions=[
        transfer_to_financial_data_agent,
        transfer_to_web_researcher,
        transfer_to_summarizer
    ]
)