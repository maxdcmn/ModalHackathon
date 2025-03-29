# Agents that read the general overview of the company and extract relevant features
# to generate the introductory paragraph and tables with general financial data.
from smolagents import CodeAgent
import json

def generate_stock_price_plot(model, daily):
    stock_price_plot_evolution_generator = CodeAgent(
        tools=[],
        name="StockPricePlotGenerator",
        model=model,
        additional_authorized_imports=["json", "matplotlib", "matplotlib.pyplot", "tikzplotlib"],
        description="Generates a stock price evolution plot inspired by financial reports.",
    )

    closing_vals = {value["close"] for value in daily}
    
    result = stock_price_plot_evolution_generator.run("""
        Given a JSON file containing daily stock price data, generate a visually appealing line plot.
        The plot should include:
        
        - A time series of the closing price of the stock.
        - A comparison index (if available) with a different color and style.
        - Key annotations such as dividends or major events if possible.
        - Proper labels, grid lines, and formatting to enhance readability.
        
        Output should be a LaTeX code that generates the desired plot.
                                                      
        The data is found in the following object:                                       
        """ + str(closing_vals))
    return result