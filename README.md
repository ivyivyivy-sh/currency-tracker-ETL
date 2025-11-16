# Currency Exchange Rate Tracker

An automated Python application that tracks daily exchange rates and stores them in an SQLite database. Perfect for learning about automation, APIs, databases, and scheduled tasks.

## Features

- **Automated Data Collection**: Fetches daily exchange rates from Frankfurter API
- **SQL Database**: Stores historical exchange rate data in SQLite
- **Error Handling**: Comprehensive exception handling and logging
- **Automated Testing**: Simple test suite to verify functionality
- **Scheduled Execution**: Ready for Windows Task Scheduler
- **Clean Code**: Well-documented and follows Python best practices

## Tracked Currencies

- **Base Currency**: USD (US Dollar)
- **Target Currencies**:
  - EUR (Euro)
  - GBP (British Pound)
  - SEK (Swedish Krona)
  - CNY (Chinese Yuan)

## currency-exchange-tracker/
├── currency_tracker.py      # Main application script
├── database.py              # Database operations
├── config.py               # Configuration settings
├── test.py          # Easy-to-run tests
├── requirements.txt        # Python dependencies
├── currency_tracker.log    # Log file (created automatically)
├── exchange_rates.db       # Database file (created automatically)
└── README.md              # This file
