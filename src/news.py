# Agents that reads the news and report on some macro data
from smolagents import CodeAgent

def get_news_reports(model, stock, news):
    headline_selector = CodeAgent(tools=[], model=model, name="headline_selector",
        description="select news article based on some meta data. Give it a json of different news articles' meta data")
    
    
    web_agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['requests', 'bs4'], name="news_reader",
        description="goes into web adresses and reads news article and extract the most important content to be used for stock analysis. Give it a list of relevant articles' web adressses")
    
    summarise_agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['requests', 'bs4'], name="news_summariser",
        description="Summarise and aggregates the news content of several news article to provide a holisitc perspective regarding the stock. Give it information extracted from articles")
    

    manager_agent = CodeAgent(
        tools=[], model=model, managed_agents=[web_agent, headline_selector, summarise_agent]
    )

    
    response = manager_agent.run(f"What is the most important news regarding stock {stock}? \n \n {news}")
    return response
    