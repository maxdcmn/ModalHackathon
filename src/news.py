# Agents that reads the news and report on some macro data
from smolagents import CodeAgent, HfApiModel, DuckDuckGoSearchTool

def get_news_reports(model, stock, news):
    # headline_selector = CodeAgent(tools=[], model=model, name="headline_selector",
    #     description="select news article based on some meta data. Give it a json of different news articles' meta data. If it is empty, let the manager know that.")
    
    
    # web_agent = CodeAgent(tools=[], model=model, additional_authorized_imports=['requests', 'bs4'], name="news_reader",
    #     description="goes into web adresses and reads news article and extract the most important content to be used for stock analysis. Give it a list of relevant articles' web adressses")
    
    # summarise_agent = CodeAgent(tools=[], model=model, name="news_summariser",
    #     description="Summarise and aggregates the news content of several news article to provide a holisitc perspective regarding the stock. Give it information extracted from articles")
    

    # manager_agent = CodeAgent(
    #     tools=[], model=model, managed_agents=[headline_selector, summarise_agent]
    # )

    
    # response = manager_agent.run(f"What is the most important news regarding stock {stock}? \n \n {news}")


    # Define the web search tool
    web_search_tool = DuckDuckGoSearchTool()

    # Create an agent that can use the web search tool
    web_agent = CodeAgent(
        tools=[web_search_tool], 
        model=model, 
        name="web_searcher",
        description="An agent that runs web searches and retrieves relevant information."
    )

    # Manager agent that delegates tasks
    manager_agent = CodeAgent(
        tools=[], 
        model=model, 
        managed_agents=[web_agent], 
        name="manager_agent",
        description="Manages other agents and delegates tasks."
    )

    # Now, let the manager agent request the web agent to search for the CEO
    response = manager_agent.run("Use web_searcher to find out who is the CEO of Hugging Face.")
    
    return response