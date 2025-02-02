import os
from dotenv import load_dotenv
load_dotenv()

config_list = [
    {"model": "gpt-4o", "api_key": os.environ["OPENAI_API_KEY"], "temperature": 0}]

llm_config = {
    "functions": [
        {
            "name": "getYahooFinance",
            "description": "Obtain .csv data from Yahoo Finance",
            "parameters": {
                "type": "object",
                "properties": {
                    "ticker": {
                        "type": "string",
                        "description": "The ticker of the stock market data to be downloaded from Yahoo Finance"
                    }
                },
                "required": ["ticker"],
            },
        },
        {
            "name": "code_executor",
            "description": "This is a python code executor that takes codes as a string and executes it.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "A string of code to be executed"
                    }
                },
                "required": ["command"],
            },
        }
    ],
    "config_list": config_list,
}
