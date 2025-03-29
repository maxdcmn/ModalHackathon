import modal
from fastapi import Response, HTTPException, Header
from smolagents import CodeAgent, HfApiModel, GradioUI
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from dotenv import load_dotenv


import json
import os
import secrets

from src.news import get_news_reports
from src.model import VLLMModalModel


load_dotenv()

# Check that your token is being loaded properly
hf_token = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
if not hf_token:
    print("WARNING: No Hugging Face token found in environment")


image = modal.Image.debian_slim(python_version="3.11.11").pip_install(["fastapi[standard]", "reportlab", "smolagents", "dotenv", "openai"])
app = modal.App(name="modal-pdf-generator", image=image)


@app.function(secrets=[modal.Secret.from_name("modal-hackathon-secrets")])    
@modal.fastapi_endpoint(method="POST", docs=True)
def generate_pdf(data: dict, x_api_key: str = Header(None)) -> Response:
    # Validate API key
    if x_api_key != os.environ.get("API_KEY"):
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    VLLM_API_KEY=os.environ["VLLM_API_KEY"]
    model = VLLMModalModel(
        api_key=VLLM_API_KEY,
        temperature=0.7,
        max_tokens=512
    )
    
    # Create a BytesIO buffer for the PDF
    buffer = BytesIO()
    
    news_info = get_news_reports(model, data.get("overview")["Name"], data.get("newsData"))
    
    # Create the PDF document
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=72,
        leftMargin=72,
        topMargin=72,
        bottomMargin=72
    )
    
    # Define styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='JsonStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        alignment=TA_LEFT,
        spaceAfter=12
    ))
    
    # Create content
    content = []
    
    # Add title
    content.append(Paragraph("Stock Analysis Data", styles['Title']))
    content.append(Spacer(1, 12))
    
    
    
    # Add timestamp if available
    timestamp = data.get('timestamp', 'Not provided')
    content.append(Paragraph(f"Report generated: {timestamp}", styles['Normal']))
    content.append(Spacer(1, 12))
    
    # Add stock symbol if available
    stock_symbol = data.get('stockSymbol', 'Not provided')
    content.append(Paragraph(f"Stock Symbol: {stock_symbol}", styles['Heading2']))
    content.append(Spacer(1, 12))
    
    content.append(Paragraph(f"{news_info}", styles['Normal']))
    # Format the JSON data for display
    formatted_json = json.dumps(data, indent=2)
    
    # Split the JSON by lines and add each piece
    content.append(Paragraph("Full JSON Data:", styles['Heading3']))
    content.append(Spacer(1, 6))
    
    # Add the JSON content - handling line breaks
    for line in formatted_json.split('\n'):
        content.append(Paragraph(line, styles['JsonStyle']))
    
    # Build the PDF
    doc.build(content)
    
    # Get the PDF content
    pdf_content = buffer.getvalue()
    buffer.close()
    
    # Return PDF response with appropriate headers
    return Response(
        content=pdf_content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=stock_report_{stock_symbol}.pdf"}
    )
