from database.querys import q_returns
from feature_engineering.returns import log_return
from feature_engineering.rolling import rolling_mean, rolling_std

def z_score_historic(df):
    returns = log_return(df)
    mean = returns.mean()
    std = returns.std()
    z_score = (returns - mean) / std

    return z_score

def z_score_mobile(df, window):
    returns = log_return(df)
    mean = rolling_mean(returns, window)
    std = rolling_std(returns, window)
    z_score = (returns - mean) / std

    return z_score
