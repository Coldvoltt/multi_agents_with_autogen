import yfinance as yf
import pandas as pd  # Import pandas for DataFrame manipulations
from datetime import datetime, timedelta
from langchain_experimental.utilities import PythonREPL


def getYahooFinance(ticker: str) -> str:
    try:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)
                      ).strftime('%Y-%m-%d')
        # Fetch stock data from Yahoo Finance
        stock_data = yf.download(
            ticker, start=start_date, end=end_date, progress=False
        )
        if stock_data.empty:
            return f"No data found for ticker '{ticker}'. Please check the ticker symbol or the date range."
        # Reset index to ensure the Date column is included
        stock_data.reset_index(inplace=True)
        # Rename columns to standard financial terms
        stock_data.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

        # Save the data to a CSV file
        stock_data.to_csv("stock_price_history.csv", index=False)

        return f"Stock price of {ticker} has been saved to stock_price_history.csv"
    except Exception as e:
        return f"An error occurred while fetching data for ticker '{ticker}': {e}"


def code_executor(command: str):
    try:
        repl = PythonREPL()
        return repl.run(command)
    except Exception as e:
        print(f"Error initializing Python REPL: {e}")
        return None
