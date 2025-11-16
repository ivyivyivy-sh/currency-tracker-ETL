#!/usr/bin/env python3
"""
Currency Exchange Rate Tracker
Automatically fetches daily exchange rates and stores them in SQLite database.
"""

import requests
import logging
from datetime import datetime
from config import API_URL, BASE_CURRENCY, TARGET_CURRENCIES, TIMEOUT
from database import create_table, insert_exchange_rate

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('currency_tracker.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def fetch_exchange_rates():
    """
    Fetch current exchange rates from the Frankfurter API.
    
    Returns:
        dict: Dictionary containing exchange rates and metadata, or None if failed
        
    Raises:
        requests.RequestException: If there's an error with the API request
    """
    try:
        logger.info(f"Fetching exchange rates for {BASE_CURRENCY} to {TARGET_CURRENCIES}")
        
        params = {
            'from': BASE_CURRENCY,
            'to': ','.join(TARGET_CURRENCIES)
        }
        
        response = requests.get(API_URL, params=params, timeout=TIMEOUT)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()
        logger.info("Successfully fetched exchange rates from API")
        return data
        
    except requests.RequestException as e:
        logger.error(f"API request failed: {e}")
        return None
    except ValueError as e:
        logger.error(f"Error parsing JSON response: {e}")
        return None

def process_and_store_rates(api_data):
    """
    Process API response and store exchange rates in database.
    
    Args:
        api_data (dict): The JSON response from the API
        
    Returns:
        bool: True if all rates were processed successfully, False otherwise
    """
    if not api_data or 'rates' not in api_data:
        logger.error("Invalid API data received")
        return False
    
    try:
        timestamp = datetime.now()
        base_currency = api_data.get('base', BASE_CURRENCY)
        rates = api_data.get('rates', {})
        
        success_count = 0
        for target_currency, rate in rates.items():
            if target_currency in TARGET_CURRENCIES:
                if insert_exchange_rate(timestamp, base_currency, target_currency, rate):
                    success_count += 1
                else:
                    logger.warning(f"Failed to insert rate for {target_currency}")
        
        logger.info(f"Successfully processed {success_count} out of {len(TARGET_CURRENCIES)} currency rates")
        return success_count > 0
        
    except Exception as e:
        logger.error(f"Error processing exchange rates: {e}")
        return False

def main():
    """
    Main function to execute the currency tracking process.
    """
    logger.info("Starting currency exchange rate tracker")
    
    try:
        # Ensure database table exists
        create_table()
        
        # Fetch exchange rates from API
        api_data = fetch_exchange_rates()
        
        if api_data:
            # Process and store the rates
            success = process_and_store_rates(api_data)
            
            if success:
                logger.info("Currency tracking completed successfully")
            else:
                logger.error("Currency tracking completed with errors")
        else:
            logger.error("Failed to fetch data from API")
            
    except Exception as e:
        logger.error(f"Unexpected error in main execution: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    exit(exit_code)