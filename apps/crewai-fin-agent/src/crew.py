from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from langchain_openai import ChatOpenAI

from tools import (
    StockPriceTool,
    CompanyProfileTool,
    FinancialRatiosTool,
    MarketCapTool,
    KeyMetricsTool,
    StockScreenerTool,
    SingleLineItemQueryTool,
    WebpageReadingTool
)

@CrewBase
class CrewaiFinAgent():
    """CrewaiFinAgent crew"""

    @agent
    def financial_data_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['financial_data_agent'],
            verbose=True,
            tools=[
                StockPriceTool(),
                CompanyProfileTool(),
                FinancialRatiosTool(),
                MarketCapTool(),
                KeyMetricsTool(),
                StockScreenerTool(),
                SingleLineItemQueryTool()
            ]
        )
    
    @agent
    def web_scraping_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['web_scraping_agent'],
            tools=[
                WebpageReadingTool()
            ]
        )
    
    @agent
    def output_summarizing_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['output_summarizing_agent'],
        )

    @task
    def gather_financial_data(self) -> Task:
        return Task(
            config=self.tasks_config['gather_financial_data']
        )

    @task
    def gather_website_information(self) -> Task:
        return Task(
            config=self.tasks_config['gather_website_information']
        )
    
    @task
    def summarize_findings(self) -> Task:
        return Task(
            config=self.tasks_config['summarize_findings']
        )

    # Define the supervisor agent separately to handle coordination
    supervisor_agent = Agent(
        role="Supervisor",
        goal="Leverage the skills of your coworkers to answer the user's query: {query}.",
        backstory="""You are a manager who oversees the workflow of the financial assistant, 
        skilled in overseeing complex workers with different skills and ensuring that you can answer the user's query with the help of the coworkers. 
        You always try to gather data using the financial data agent and / or web scraping agent first.
        After gathering the data, you must delegate to the output summarizing agent to create a comprehensive report instead of answering the user's query directly.""",
        verbose=True,
        llm=ChatOpenAI(model="gpt-4o", temperature=0.5),
        allow_delegation=True,
    )

    @crew
    def crew(self) -> Crew:
        """Creates the CrewaiFinAgent crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            manager_agent=self.supervisor_agent,
            memory=True, # creates memory files in "CREWAI_STORAGE_DIR" folder
            verbose=True, # necessary for memory
        )