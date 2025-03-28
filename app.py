import warnings
import gradio as gr
from crew import analyze_business_data
import pandas as pd
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def generate_pdf_report(analysis_result):
    if not analysis_result or analysis_result.startswith("Error") or analysis_result.startswith("Please"):
        return "Cannot generate PDF report without valid analysis results."
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"business_report_{timestamp}.pdf"
    
    c = canvas.Canvas(filename)
    c.setFont("Helvetica", 16)
    c.drawString(50, 800, "Business Intelligence Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, 770, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    y = 730
    for line in analysis_result.split('\n'):
        if y < 50:
            c.showPage()
            y = 800
        c.drawString(50, y, line)
        y -= 15
    
    c.save()
    return f"PDF report generated: {filename}"

def create_action_items(analysis_result):
    if not analysis_result or analysis_result.startswith("Error") or analysis_result.startswith("Please"):
        return "Cannot create action items without valid analysis results."
    
    action_items = [
        "🎯 Review top-performing products and optimize inventory",
        "📈 Analyze marketing campaign effectiveness",
        "💰 Identify cost-saving opportunities",
        "🔄 Optimize operational processes",
        "📊 Monitor market trends and adjust strategy"
    ]
    
    return "\n\n**Recommended Action Items:**\n" + "\n".join(action_items)

def process_query(csv_file, query):
    if csv_file is None:
        return "⚠️ Please upload a CSV file first."
    if not query.strip():
        return "❓ Please enter a question about your data."
    
    try:
        file_extension = os.path.splitext(csv_file.name)[1].lower()
        if file_extension != '.csv':
            return "⚠️ Invalid file format. Please upload a CSV file only."
        
        try:
            df = pd.read_csv(csv_file.name)
        except pd.errors.EmptyDataError:
            return "⚠️ The uploaded CSV file is empty. Please upload a file with data."
        except pd.errors.ParserError:
            return "⚠️ Unable to parse the CSV file. Please ensure it's a valid CSV format."
        except Exception as e:
            return f"⚠️ Error reading the CSV file: {str(e)}"
            
        required_columns = [
            "Date", "Product", "Region", "Sales_Amount", 
            "Marketing_Campaign", "Customer_ACQ_Cost", "Support_Tickets",
            "Operational_Cost", "Profit_Margin", "Market_Trend"
        ]
        
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return f"📋 CSV file is missing required columns: {', '.join(missing_columns)}\nPlease ensure your file contains all required columns."
        
        result = analyze_business_data(csv_file.name, query)
        return result
    
    except Exception as e:
        return f"Error processing file: {str(e)}"

with gr.Blocks(theme=gr.themes.Soft()) as app:
    gr.Markdown("""
    # 🤖 Business Intelligence Assistant
    Upload your business data (CSV) and ask questions to get AI-powered insights from our team of specialized agents:
    - 📊 Sales Analyst
    - 📈 Marketing Strategist
    - 💰 Finance Guardian
    - ⚙️ Operations Optimizer
    - 🔍 Research Coordinator
    """)
    
    with gr.Row():
        file_input = gr.File(
            label="Upload CSV",
            file_types=["csv"],
            file_count="single",
            type="filepath",
            scale=2
        )
        gr.Markdown(
            "📋 Please upload a CSV file with the required columns: Date, Product, Region, Sales_Amount, Marketing_Campaign, Customer_ACQ_Cost, Support_Tickets, Operational_Cost, Profit_Margin, Market_Trend"
        )
    
    with gr.Row():
        query_input = gr.Textbox(
            label="Ask a question about your data",
            placeholder="e.g., Show top 3 products by profitability, Which region has best marketing ROI?",
            lines=2
        )
    
    with gr.Row():
        submit_btn = gr.Button("🔄 Get Insights", variant="primary")
    
    with gr.Row():
        output = gr.Markdown(label="Analysis Results")
    
    with gr.Row():
        gr.Markdown("### 🎯 Action Center")
    
    with gr.Row():
        pdf_btn = gr.Button("📄 Generate PDF Report", variant="secondary")
        action_btn = gr.Button("✨ Create Action Items", variant="secondary")
    
    with gr.Row():
        action_output = gr.Markdown(label="Action Center Output")
    
    submit_btn.click(
        fn=process_query,
        inputs=[file_input, query_input],
        outputs=[output]
    )
    
    pdf_btn.click(
        fn=generate_pdf_report,
        inputs=[output],
        outputs=[action_output]
    )
    
    action_btn.click(
        fn=create_action_items,
        inputs=[output],
        outputs=[action_output]
    )

if __name__ == "__main__":
    app.launch()
