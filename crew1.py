from crewai import Crew, Agent, Task, LLM
from crewai_tools import CSVSearchTool, SerperDevTool
from langchain_huggingface import HuggingFaceEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()
import warnings
warnings.filterwarnings("ignore")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

llm = LLM(
    temperature=0,
    model="groq/gemma2-9b-it",
    api_key=GROQ_API_KEY,
    max_tokens=4000,
    frequency_penalty=0.1,
    seed=42
    )
config = dict(
    llm=dict(
        provider="groq",
        config=dict(
            model="groq/llama-guard-3-8b",
            api_key=GROQ_API_KEY,
            max_tokens=4000,

        ),
    ),
    embedder=dict(
        provider="huggingface",
        config=dict(
            model="sentence-transformers/all-MiniLM-L6-v2"
        ),
    ),
)

tool = SerperDevTool(
    api_key=SERPER_API_KEY,
    search_url="https://google.serper.dev/scholar",
    n_results=2,
)


sales_tool = CSVSearchTool(csv='sales_data.csv', config=config)
marketing_tool = CSVSearchTool(csv='marketing_campaigns.csv', config=config)
support_tool = CSVSearchTool(csv='customer_support.csv', config=config)
finance_tool = CSVSearchTool(csv='financials.csv', config=config)


sales_analyst = Agent(
    role='Senior Sales Analyst',
    goal='Maximize sales efficiency and revenue',
    backstory='Experienced in sales data analysis and optimization',
    llm=llm,
    tools=[sales_tool],
    verbose=True,
    max_itr=5,
    respect_context_window=True,
)

marketing_strategist = Agent(
    role='Digital Marketing Expert',
    goal='Optimize advertising ROI',
    backstory='Proficient in digital marketing strategies',
    llm=llm,
    tools=[marketing_tool],
    verbose=True,
    max_itr=5,
    respect_context_window=True,
)

support_manager = Agent(
    role='Customer Experience Lead', 
    goal='Improve support quality',
    backstory='Skilled in customer support management',
    llm=llm,
    tools=[support_tool],
    verbose=True,
    max_itr=5,
    respect_context_window=True,
)

finance_auditor = Agent(
    role='Financial Controller',
    goal='Ensure fiscal health',
    backstory='Experienced in financial analysis and control',
    llm=llm,
    tools=[finance_tool],
    verbose=True,
    max_itr=5,
    respect_context_window=True,
)


sales_task = Task(
    description='Analyze last quarter sales data to identify top 3 performing regions and forecast next quarter sales',
    agent=sales_analyst,
    expected_output='Table with regional performance metrics and forecast numbers'
)

marketing_task = Task(
    description='Calculate ROI for each marketing channel and recommend budget reallocation',
    agent=marketing_strategist,
    expected_output='Ranked list of channels by ROI with percentage allocation suggestions'
)

support_task = Task(
    description='Identify support categories with resolution times exceeding 24hrs and low satisfaction scores',
    agent=support_manager,
    expected_output='List of problem categories with improvement recommendations'
)

finance_task = Task(
    description='Analyze monthly financials to find cost optimization opportunities without impacting R&D',
    agent=finance_auditor,
    expected_output='Detailed cost breakdown with savings suggestions'
)


business_crew = Crew(
    agents=[sales_analyst, marketing_strategist, support_manager, finance_auditor],
    tasks=[sales_task, marketing_task, support_task, finance_task],
    verbose=True
)

result = business_crew.kickoff()
print("\n\n=== FINAL REPORT ===")
print(result)
