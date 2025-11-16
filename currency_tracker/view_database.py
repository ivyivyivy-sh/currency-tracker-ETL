import sqlite3
from config import DATABASE_FILE

def view_database():
    """Simple function to view the contents of the database"""
    try:
        with sqlite3.connect(DATABASE_FILE) as conn:
            cursor = conn.cursor()
            
            # Show all tables
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            print("Tables in database:")
            for table in tables:
                print(f" - {table[0]}")
            
            # Show data from exchange_rates table
            print("\nLatest exchange rates:")
            cursor.execute('''
                SELECT timestamp, base_currency, target_currency, exchange_rate 
                FROM exchange_rates 
                ORDER BY timestamp DESC 
                LIMIT 10
            ''')
            rows = cursor.fetchall()
            
            for row in rows:
                print(f"{row[0]} | {row[1]}->{row[2]} | {row[3]:.4f}")
                
    except sqlite3.Error as e:
        print(f"Error accessing database: {e}")

if __name__ == "__main__":
    view_database()