import pandas as pd
from database.querys import q_returns_indexed
from feature_engineering.returns import log_return

def returns_correlation(assets):
    df = pd.DataFrame()
    for ticker, asset in assets.items():
        df[ticker] = log_return(asset).rename(ticker)
    correlation = df.corr()
    return correlation

def prices_correlation(assets):
    df = pd.DataFrame()
    for ticker, asset in assets.items():
        df[ticker] = asset['adj_close']
    correlation = df.corr()
    return correlation

if __name__ == "__main__":
    assets={
        'ASML' : q_returns_indexed('ASML', '1y'),
        'SPY' : q_returns_indexed('SPY', '1y')
    }

    correlation_returns = returns_correlation(assets)
    print(correlation_returns)

    print()

    correlations_prices = prices_correlation(assets)
    print(correlations_prices)