from database.db_connection import get_engine
import pandas as pd

PERIOD_MAP = {
    "1d": "1 day","5d": "5 days","1mo": "1 month","3mo": "3 month","6mo": "6 months",
    "1y": "1 year","2y": "2 years","5y": "5 years","10y": "10 years"
}


'QUERY RETURNS-----------------------------------------------------------------------------------------------------------------------------------------------------'
def q_returns(ticker,period):
   
    if period == 'max':
        date_filter = ""
    elif period == 'ytd':
        date_filter = "AND date >= DATE_TRUNC('year', CURRENT_DATE)"
    else:
        date_filter = f"AND date > (CURRENT_DATE - INTERVAL '{PERIOD_MAP[period]}')" 

    connection = get_engine()

    read = pd.read_sql((f"""SELECT adj_close FROM stock_prices WHERE
                        ticker = '{ticker}'  {date_filter}
                        """), connection)
    return read

'QUERY RETURNS INDEXED-----------------------------------------------------------------------------------------------------------------------------------------------------'

def q_returns_indexed(ticker,period):
   
    if period == 'max':
        date_filter = ""
    elif period == 'ytd':
        date_filter = "AND date >= DATE_TRUNC('year', CURRENT_DATE)"
    else:
        date_filter = f"AND date > (CURRENT_DATE - INTERVAL '{PERIOD_MAP[period]}')" 

    connection = get_engine()

    read = pd.read_sql(f"""SELECT date, adj_close FROM stock_prices 
                    WHERE ticker = '{ticker}' {date_filter}
                    ORDER BY date
                    """, connection, index_col='date')
    return read

'QUERY FOR CHARTS'

def q_price_chart(ticker, period):

    if period == 'max':
        date_filter = ""
    elif period == 'ytd':
        date_filter = "AND date >= DATE_TRUNC('year', CURRENT_DATE)"
    else:
        date_filter = f"AND date > (CURRENT_DATE - INTERVAL '{PERIOD_MAP[period]}')" 

    connection = get_engine()

    read = pd.read_sql(f"""SELECT date, adj_close, close, volume FROM stock_prices 
                    WHERE ticker = '{ticker}' {date_filter}
                    ORDER BY date
                    """, connection, index_col='date')
    return read
