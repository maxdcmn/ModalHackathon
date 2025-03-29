# Agents that read the general overview of the company and extract relevant features
# to generate the introductory paragraph and tables with general financial data.
from smolagents import CodeAgent
import json

def generate_stock_price_plot(model, daily):
    stock_price_plot_evolution_generator = CodeAgent(
        name="StockPricePlotGenerator",
        model=model,
        description="Generates a stock price evolution plot inspired by financial reports.",
    )
    
    result = stock_price_plot_evolution_generator.run("""
        Given a JSON file containing daily stock price data, generate a visually appealing line plot similar to the provided example.
        The plot should include:
        
        - A time series of the closing price of the stock.
        - A comparison index (if available) with a different color and style.
        - Key annotations such as dividends or major events if possible.
        - Proper labels, grid lines, and formatting to enhance readability.
        
        Output should be a rendered plot image.
                                                      
        The data is found in the following                                        
        """ + json.dumps(daily))
    return result