"""
Configuration settings for the Currency Exchange Rate Tracker.
"""

# API Configuration
API_URL = "https://api.frankfurter.app/latest"
BASE_CURRENCY = "USD"
TARGET_CURRENCIES = ["EUR", "GBP", "SEK", "CNY"]

# Database Configuration
DATABASE_FILE = "exchange_rates.db"

# Logging Configuration
LOG_FILE = "currency_tracker.log"
LOG_LEVEL = "INFO"

# Request Configuration
TIMEOUT = 10  # seconds