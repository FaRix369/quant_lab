from pipelines.stock_collector.api_client import history_price
from pipelines.stock_collector.transform import transform_data
from pipelines.stock_collector.db_writer import writer

def collect (ticker, period):
    print(f'Collecting {ticker} from {period}')
    data = history_price(ticker, period)
    if data is None:
        print(f'Collection failed for {ticker}. Check ticker symbol and period.')
        return None
    else:
        df = transform_data(data, ticker)
        writer(df)
        return df
