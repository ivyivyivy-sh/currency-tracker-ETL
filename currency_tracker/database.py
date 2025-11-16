"""
Database operations for the Currency Exchange Rate Tracker.
"""

import sqlite3
import logging
from datetime import datetime
from config import DATABASE_FILE

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

def create_table():
    """
    Create the exchange_rates table if it doesn't exist.
    
    Raises:
        sqlite3.Error: If there's an error creating the table
    """
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exchange_rates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp DATETIME NOT NULL,
                    base_currency TEXT NOT NULL,
                    target_currency TEXT NOT NULL,
                    exchange_rate REAL NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
            logger.info("Database table verified/created successfully")
            
    except sqlite3.Error as e:
        logger.error(f"Error creating database table: {e}")
        raise

def insert_exchange_rate(timestamp, base_currency, target_currency, exchange_rate):
    """
    Insert a new exchange rate record into the database.
    
    Args:
        timestamp (datetime): The timestamp of the exchange rate
        base_currency (str): The base currency code (e.g., 'USD')
        target_currency (str): The target currency code (e.g., 'EUR')
        exchange_rate (float): The exchange rate value
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exchange_rates (timestamp, base_currency, target_currency, exchange_rate)
                VALUES (?, ?, ?, ?)
            ''', (timestamp, base_currency, target_currency, exchange_rate))
            conn.commit()
            logger.info(f"Successfully inserted rate: {base_currency}->{target_currency} = {exchange_rate}")
            return True
            
    except sqlite3.Error as e:
        logger.error(f"Error inserting exchange rate: {e}")
        return False

def get_latest_rates():
    """
    Get the latest exchange rates for each currency pair.
    
    Returns:
        list: List of tuples containing the latest rates
    """
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT base_currency, target_currency, exchange_rate, timestamp
                FROM exchange_rates 
                WHERE timestamp = (
                    SELECT MAX(timestamp) FROM exchange_rates AS e2 
                    WHERE e2.base_currency = exchange_rates.base_currency 
                    AND e2.target_currency = exchange_rates.target_currency
                )
                ORDER BY target_currency
            ''')
            return cursor.fetchall()
            
    except sqlite3.Error as e:
        logger.error(f"Error fetching latest rates: {e}")
        return []