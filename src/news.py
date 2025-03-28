# Agents that reads the news and report on some macro data
from smolagents import CodeAgent, VisitWebpageTool, FinalAnswerTool



def get_news_reports(model, stock, news):    
    web_agent = CodeAgent(
        tools=[VisitWebpageTool()], 
        model=model, 
        name="URL_reader",
        description="""Extract key information from a provide URL.""")
    
    manager_agent = CodeAgent(
        tools=[FinalAnswerTool()], 
        model=model, 
        name="final_answer_provider",
        managed_agents=[web_agent],
        description="""Answers the prompt by deligating the process""")
    
    

    # Now, let the manager agent request the web agent to search for the CEO
    response = manager_agent.run("Use web_searcher to find out who is the CEO of Hugging Face.")
    
    return manager_agent.run("what is the first paragraph of this website (ignore the headers)? https://www.ehl.lu.se/studera-vid-ekonomihogskolan/studentwebben/studentliv/finansforeningen-linc")