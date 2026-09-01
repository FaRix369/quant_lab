import numpy as np
from database.querys import q_returns
from feature_engineering.returns import log_return


def historic_simple_volatility (return_log):
    hs_volatility = (return_log.std()) * (252**0.5)
    return hs_volatility

def anualized_volatility(hs_volatility):
    volatility_anual = hs_volatility * np.sqrt(252)
    return volatility_anual

def rolling_volatility(return_log, window):
    volatility_rolling = return_log.rolling(window).std()
    return volatility_rolling

def ewma_volatility(return_log, lam=0.94):
    volatility_ewma = return_log.ewm(span=2/(1-lam)-1).std()
    return volatility_ewma
    