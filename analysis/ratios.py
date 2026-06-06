import pandas as pd
from database.querys import q_returns, q_returns_indexed
from cli.cli import get_ticker_period
from feature_engineering.volatility import historic_simple_volatility
from feature_engineering.returns import log_return_digit, log_return
from feature_engineering.drawdown import max_drawdown, function_drawdown


def sharpe_ratio(df, rf=0.05):
    return_log = log_return(df)
    rf_period = (1 + rf)**(len(df)/252)-1

    rp = log_return_digit(df)
    sigma =  historic_simple_volatility(return_log)

    sharpe = (rp - rf_period) / sigma
    return sharpe

def sortino_ratio(df, rf=0.05):
    return_log = log_return(df)
    negative_return_log = return_log[return_log < 0]
    rf_period = (1 + rf)**(len(df)/252)-1

    rp = log_return_digit(df)
    sigma =  historic_simple_volatility(negative_return_log)

    sortino = (rp - rf_period) / sigma
    return sortino

def calmar_ratio(df):
    rp = log_return_digit(df)
    drawdown = function_drawdown(df)
    max_dd = max_drawdown(drawdown)

    calmar = rp / abs(max_dd)
    return calmar

def beta_ratio(df, benchmark):
    rp = log_return(df)
    rm = log_return(benchmark)

    rp, rm = rp.align(rm, join='inner')

    beta = (rp.cov(rm)) / rm.var()
    return beta

def alpha_ratio(df, benchmark, rf=0.05):
    rp = log_return_digit(df)
    rm = log_return_digit(benchmark)
    beta = beta_ratio(df, benchmark)

    alpha = rp - (rf + beta *(rm - rf))
    return alpha


if __name__ == "__main__":
    ticker, period = get_ticker_period()
    read = q_returns(ticker,period)
    read_indexed = q_returns_indexed(ticker, period)

    benchmark = q_returns_indexed(ticker='SPY', period=period)

    print('SHARPE RATIO:')
    sharpe = sharpe_ratio(read)
    print(sharpe)
    print()
    print('SORTINO RATIO:')
    sortino = sortino_ratio(read)
    print(sortino)
    print()
    print('CALMAR RATIO:')
    calmar = calmar_ratio(read)
    print(calmar)
    print()
    print('BETA RATIO:')
    beta = beta_ratio(read_indexed, benchmark)
    print(beta)
    print()
    print('ALPHA RATIO:')
    alpha = alpha_ratio(read_indexed, benchmark)
    print(alpha)