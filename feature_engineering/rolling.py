import pandas as pd
from database.querys import q_returns


def rolling_mean(df, window):
    if isinstance(df, pd.DataFrame):
        adj_close = df['adj_close']
        mean_rolling = adj_close.rolling(window).mean()
    else:
        mean_rolling = df.rolling(window).mean()

    return mean_rolling

def rolling_std(df, window):
    if isinstance(df, pd.DataFrame):
        adj_close = df['adj_close']
        std_rolling = adj_close.rolling(window).std()
    else:
        std_rolling = df.rolling(window).std()

    return std_rolling

def rolling_min(df, window):
    if isinstance(df, pd.DataFrame):
        adj_close = df['adj_close']
        min_rolling = adj_close.rolling(window).min()
    else:
        min_rolling = df.rolling(window).min()
    return min_rolling

def rolling_max(df, window):
    if isinstance(df, pd.DataFrame):
        adj_close = df['adj_close']
        max_rolling = adj_close.rolling(window).max()
    else:
        max_rolling = df.rolling(window).max()
    return max_rolling