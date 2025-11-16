#!/usr/bin/env python3
"""
Quick test - just see if everything works
"""

print("🚀 Quick Test - Currency Tracker")

try:
    # Test 1: Import modules
    from database import create_table
    from currency_tracker import fetch_exchange_rates
    print("✅ All modules imported successfully")
    
    # Test 2: Create database
    create_table()
    print("✅ Database setup complete")
    
    # Test 3: Try API call
    print("🌐 Testing API connection...")
    rates = fetch_exchange_rates()
    
    if rates:
        print("✅ API connection successful!")
        print("📊 Current rates:")
        for currency, rate in rates['rates'].items():
            print(f"   USD to {currency}: {rate}")
    else:
        print("❌ API connection failed")
        
except Exception as e:
    print(f"❌ Test failed: {e}")