import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine

route = os.path.abspath(__file__)
db_route = os.path.dirname(os.path.dirname(route)) #jumps on the route (.env)
final_route = os.path.join(db_route, '.env')
load_dotenv(final_route)

def connection_database():
    connection = psycopg2.connect(host=os.getenv('HOST'), port=os.getenv('PORT'), database=os.getenv('DB_NAME'), user=os.getenv('DB_USER'), password=os.getenv('DB_PASSWORD'))

    return connection

def get_engine():
    engine = create_engine(f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}")
    return engine

def get_status():
    try:
        conn = connection_database()
        cursor = conn.cursor()
        
        # query 1: tickers
        cursor.execute("SELECT COUNT(DISTINCT ticker) FROM stock_prices")
        ticker_count = cursor.fetchone()[0]
        
        # query 2: date range
        cursor.execute("SELECT MIN(date), MAX(date) FROM stock_prices")
        date_range = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print(f"Database: connected")
        print(f"Tickers: {ticker_count}")
        print(f"Date range: {date_range[0]} → {date_range[1]}")
        
    except Exception as e:
        print(f"Database: disconnected — {e}")
#assuming that it will always connect to the same database