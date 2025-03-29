# Agents that read the general overview of the company and extract relevant features
# to generate the introductory paragraph and tables with general financial data.
from smolagents import CodeAgent
import json

def extract_company_info(model, overview):
    general_info_agent = CodeAgent(
        tools=[],
        name="CompanyInfoExtractor",
        model=model,
        additional_authorized_imports=["json"],
        description="""Given a JSON file containing general information of the stock, generate an introductory paragraph providing that information using formal language.
        """
    )

    web_agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['requests', 'bs4'], name="webpage_reader",
        description="goes into the web adress of the company and extracts the most important content to be used for a general overview of the company's goals, sector, history, number of customers, etc. Give it the web address.")
    
    manager_agent = CodeAgent(
        tools=[], 
        model=model, 
        managed_agents=[general_info_agent, web_agent], 
        additional_authorized_imports=['requests', 'bs4', "json"],
        name="manager_agent",
        description="Manages other agents and delegates tasks."
    )

    financial_tables_agent = CodeAgent(
        name="FinancialTablesExtractor",
        tools=[],
        model=model,
        additional_authorized_imports=["json"],
        description="""Extracts financial data necessary to generate market data, forecast, and key metrics tables.
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
        """
    )

    dic = {key: overview[key] for key in ["Symbol","AssetType","Name","Description","Sector","Industry","OfficialSite","MarketCapitalization"]}
    dic2 = dict(list(overview.items())[4:])
    print(dic2)

    result_tables = financial_tables_agent.run("""
        Generate LaTeX code that makes a table with the following data: 
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
                                               
        Given the following json file: """ + json.dumps(dic2))
    
    result_overview = manager_agent.run("Write a formal paragraph explaining the information from the given json object and search additional relevant information on their webpage:  " + json.dumps(dic))
    return result_overview, result_tables