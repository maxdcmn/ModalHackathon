# Agents that read the general overview of the company and extract relevant features
# to generate the introductory paragraph and tables with general financial data.
from smolagents import CodeAgent
import json

def extract_company_info(model, overview):
    general_info_agent = CodeAgent(
        name="CompanyInfoExtractor",
        model=model,
        description="Extracts key general information about a company for use in financial reports.",
        instructions="""
        Given a JSON file containing detailed company information, extract the following key attributes:
        - Company name
        - Description
        - Sector and Industry
        - Market Capitalization
        - Revenue (TTM)
        - Profit Margin
        - Official Website
        
        Format the output as a structured dictionary.
        """
    )

    web_agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['requests', 'bs4'], name="webpage_reader",
        description="goes into the web adress of the company and other relevant websites with information regarding the company (like Wikipedia) and extracts the most important content to be used for a general overview of the company's goals, sector, history, number of customers, etc. Give it the web address and name of the company.")
    
    summarise_agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['requests', 'bs4'], name="overview_summariser",
        description="Summarise and aggregates the content of webpages with relevant information regarding the company of interest to provide a general overview of the company's goals, sector, history, etc. Give it information extracted from webpages.")
    
    manager_agent = CodeAgent(
        tools=[], model=model, managed_agents=[web_agent, general_info_agent, summarise_agent]
    )

    financial_tables_agent = CodeAgent(
        name="FinancialTablesExtractor",
        model=model,
        description="Extracts financial data necessary to generate market data, forecast, and key metrics tables.",
        instructions="""
        Given a JSON file containing company financial data, extract and structure the relevant information into three categories:
        
        1. Market Data:
           - Exchange
           - Shares Outstanding (converted to millions)
           - Market Capitalization (converted to millions)
           - Enterprise Value (if available, converted to millions)

        2. Forecast Data:
           - Total Revenue
           - Revenue Growth
           - Gross Profit
           - Gross Margin
           - EBITDA
           - EBITDA Margin
           - EBIT
           - EBIT Margin

        3. Key Metrics:
           - EV/EBITDA
           - EV/EBIT
           - ND/EBITDA (if available, otherwise mark as 'Neg.')
           - P/E Ratio
           - P/S Ratio
           - EPS
        
        Format the output as a structured dictionary suitable for generating tables.
        """
    )
    
    result_overview = manager_agent.run(json.dumps(overview))
    result_tables = financial_tables_agent.run(json.dumps(overview))
    return json.loads(result_overview), json.loads(result_tables)