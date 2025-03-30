from crewai import Crew, Agent, Task, LLM
from crewai_tools import CSVSearchTool, SerperDevTool
import os
import time
import traceback
from dotenv import load_dotenv
import warnings
import gradio as gr
import sys

load_dotenv()
warnings.simplefilter("ignore")

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

groq_models = [
    "groq/llama3-8b-8192",
    "groq/deepseek-r1-distill-qwen-32b",
    "groq/gemma2-9b-it"
]

model_Idx = 0
backoff_time = 1
MAX_RETRIES = 10

def initialize_llm():
    global model_Idx
    return LLM(
        temperature=0,
        model=groq_models[model_Idx],
        api_key=GROQ_API_KEY,
        max_tokens=2048,
        frequency_penalty=0.1,
        request_timeout=20
    )

config = {
    "llm": {
        "provider": "groq",
        "config": {
            "model": "groq/llama-guard-3-8b",
            "api_key": GROQ_API_KEY,
            "max_tokens": 512,
        },
    },
    "embedder": {
        "provider": "huggingface",
        "config": {
            "model": "sentence-transformers/all-MiniLM-L6-v2"
        },
    },
}

sales_tool = CSVSearchTool(csv='sales_data.csv', config=config)
marketing_tool = CSVSearchTool(csv='marketing_campaigns.csv', config=config)
support_tool = CSVSearchTool(csv='customer_support.csv', config=config)
finance_tool = CSVSearchTool(csv='inancials.csv', config=config)

tool = SerperDevTool(
    api_key=SERPER_API_KEY,
    n_results=2,
    timeout=12
)


sales_analyst = Agent(
    role='Sales Strategist',
    goal='Identify sales growth opportunities',
    backstory='Experienced in market analysis and revenue optimization',
    llm=initialize_llm(),
    tools=[sales_tool],
    verbose=True,
    max_rpm=150
)

marketing_specialist = Agent(
    role='Marketing Analyst',
    goal='Optimize marketing campaigns',
    backstory='Digital marketing expert with SEO and SEM experience',
    llm=initialize_llm(),
    tools=[tool, marketing_tool],
    verbose=True,
    max_rpm=150
)

customer_support_analyst = Agent(
    role='Customer Support Manager',
    goal='Imporve customer support efficiency',
    backstory='Customer support specialist with a focus on resolving issues quickly',
    llm=initialize_llm(),
    tools=[support_tool],
    verbose=True,
    max_rpm=150
)

finance_analyst = Agent(
    role='Financial Advisor',
    goal='Analyze financial health and costs',
    backstory='CPA with budget optimization expertise',
    llm=initialize_llm(),
    tools=[finance_tool],
    verbose=True,
    max_rpm=150
)

sales_analysis_task = Task(
    description="""Analyze sales data. Focus on regional performance and product sales trends.""",
    agent=sales_analyst,
    expected_output="""# Sales Analysis
- Key metrics
- Analysis
- Recommendations"""
)

marketing_analysis_task = Task(
    description="""Analyze marketing campaign effectiveness and ROI by channel.""",
    agent=marketing_specialist,
    expected_output="""# Marketing Analysis
- Key metrics
- Analysis
- Recommendations"""
)

support_analysis_task = Task(
    description="""Analyze customer support efficiency and satisfaction metrics.""",
    agent=customer_support_analyst,
    expected_output="""# Support Analysis
- Key metrics
- Analysis
- Recommendations"""
)

finance_analysis_task = Task(
    description="""Analyze financial indicators and cost optimization opportunities.""",
    agent=finance_analyst,
    expected_output="""# Financial Analysis
- Key metrics
- Analysis
- Recommendations"""
)

business_insights_task = Task(
    description="""Combine all analyses into a comprehensive business report.""",
    agent=finance_analyst,
    context=[sales_analysis_task, marketing_analysis_task, support_analysis_task, finance_analysis_task],
    expected_output="""# Business Report
- Summary
- Analysis
- Recommendations"""
)

optimization_task = Task(
    description="""Create a strategic optimization plan based on the business analysis.""",
    agent=finance_analyst,
    context=[business_insights_task],
    expected_output="""# Optimization Strategy
- Sales strategies
- Marketing recommendations
- Support improvements
- Financial planning
- Timeline"""
)

business_analytics_crew = Crew(
    agents=[sales_analyst, marketing_specialist, customer_support_analyst, finance_analyst],
    tasks=[sales_analysis_task, marketing_analysis_task, support_analysis_task, finance_analysis_task, business_insights_task, optimization_task],
    verbose=True,
    process="sequential",
    manager_llm=initialize_llm(),
    max_rpm=150,
    cache=True
)

def execute_analysis():
    global model_Idx, backoff_time
    retries = 0
    
    while retries < MAX_RETRIES:
        try:
            start_time = time.time()
            result = business_analytics_crew.kickoff()
            print(f"Analysis completed in {time.time() - start_time:.2f}s")
            return result
        except Exception as e:
            if "rate_limit" in str(e).lower():
                model_Idx = (model_Idx + 1) % len(groq_models)
                
                updated_llm = initialize_llm()
                for agent in business_analytics_crew.agents:
                    agent.llm = updated_llm
                business_analytics_crew.manager_llm = updated_llm
                
                backoff_time = min(30, backoff_time * 1.5)
                time.sleep(backoff_time)
            else:
                time.sleep(2)
            retries += 1
    
    raise Exception("Maximum retry attempts reached")

last_analysis_result = None

def run_analysis_and_save():
    global last_analysis_result
    try:
        results = execute_analysis()
        last_analysis_result = results
        return f"{results}"
    except Exception as e:
        return f"Analysis failed: {str(e)}"


def create_gradio_interface():
    with gr.Blocks(title="Business Analytics Dashboard") as app:
        gr.Markdown("# Multi-Agent Business Analytics System")
        
        with gr.Tab("Run Analysis"):
            gr.Markdown("""
            ### Generate Business Analysis Report
            
            This will run a comprehensive business analysis using multiple AI agents:
            - Sales Strategist: Identifies sales growth opportunities
            - Marketing Analyst: Optimizes marketing campaigns
            - Customer Support Manager: Improves customer support efficiency
            - Financial Advisor: Analyzes financial health and costs
            
            The analysis may take several minutes to complete.
            """)
            
            with gr.Row():
                run_button = gr.Button("Run Business Analysis", variant="primary")
            
            output = gr.Markdown()
            run_button.click(fn=run_analysis_and_save, outputs=output)
        
    return app

if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--no-ui":
            results = execute_analysis()
            print("\n=== FINAL ANALYSIS REPORT ===\n")
            print(results)
        else:
            app = create_gradio_interface()
            app.launch(share=False)
    except Exception as e:
        print(f"Application failed: {e}")
