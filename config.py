"""
Configuration file for Deal Analyzer Agent
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")

# RapidAPI Realtor Config
RAPIDAPI_HOST = "realty-in-us.p.rapidapi.com"
RAPIDAPI_BASE_URL = f"https://{RAPIDAPI_HOST}"

# DeepSeek API Config
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

# Investment Analysis Defaults
DEFAULT_HOLDING_PERIOD = 6  # months
DEFAULT_FINANCING_RATE = 0.08  # 8% interest
DEFAULT_CLOSING_COSTS_PERCENT = 0.03  # 3% of purchase price
DEFAULT_PROFIT_MARGIN_TARGET = 0.20  # 20% minimum profit margin
ARV_MULTIPLIER = 0.70  # 70% rule for fix-and-flip
