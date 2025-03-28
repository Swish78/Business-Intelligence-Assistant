from crewai import Agent, Task, Crew, LLM
from crewai_tools import CSVSearchTool
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm = LLM(
    temperature=0, 
    model="groq/deepseek-r1-distill-qwen-32b",
    api_key=GROQ_API_KEY
)

csv_tool = CSVSearchTool(
    config=dict(
        llm=dict(
            provider="groq",
            config=dict(
                model="deepseek-r1-distill-qwen-32b",
            ),
        ),
        embedder=dict(
            provider="huggingface",
            config=dict(
                model="sentence-transformers/all-MiniLM-L6-v2"
            ),
        ),
    )
)

sales_analyst = Agent(
    role='Sales Analyst',
    goal='Analyze sales data to uncover performance insights',
    backstory='Expert in sales analytics with deep understanding of revenue generation',
    verbose=True,
    llm=llm,
    tools=[csv_tool]
)

marketing_strategist = Agent(
    role='Marketing Strategist',
    goal='Evaluate marketing performance and identify optimal channels',
    backstory='Strategic marketing expert specializing in ROI analysis',
    verbose=True,
    llm=llm,
    tools=[csv_tool]
)

finance_guardian = Agent(
    role='Finance Guardian',
    goal='Monitor financial health and identify fiscal opportunities',
    backstory='Experienced financial analyst with keen eye for economic trends',
    verbose=True,
    llm=llm,
    tools=[csv_tool]
)

operations_optimizer = Agent(
    role='Operations Optimizer',
    goal='Analyze operational efficiency and identify improvements',
    backstory='Supply chain and operational efficiency expert',
    verbose=True,
    llm=llm,
    tools=[csv_tool]
)

research_coordinator = Agent(
    role='Research Coordinator',
    goal='Provide contextual market intelligence',
    backstory='Market research specialist connecting internal data with external trends',
    verbose=True,
    llm=llm,
    tools=[csv_tool]
)

def analyze_business_data(csv_path, query):
    tasks = [
        Task(
            description=f"Analyze sales performance metrics and identify top products from {csv_path}. Query: {query}",
            agent=sales_analyst
        ),
        Task(
            description=f"Evaluate marketing campaign effectiveness and ROI from {csv_path}. Query: {query}",
            agent=marketing_strategist
        ),
        Task(
            description=f"Review financial patterns and identify opportunities from {csv_path}. Query: {query}",
            agent=finance_guardian
        ),
        Task(
            description=f"Analyze operational efficiency and supply chain metrics from {csv_path}. Query: {query}",
            agent=operations_optimizer
        ),
        Task(
            description=f"Provide market context and competitive insights from {csv_path}. Query: {query}",
            agent=research_coordinator
        )
    ]

    crew = Crew(
        agents=[sales_analyst, marketing_strategist, finance_guardian, 
               operations_optimizer, research_coordinator],
        tasks=tasks,
        verbose=True
    )

    result = crew.kickoff()
    return result


