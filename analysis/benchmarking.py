from feature_engineering.returns import log_return
from database.querys import q_returns_indexed

def excess_return(rp, rm):
    rp, rm = rp.align(rm, join='inner')
    return rp - rm

def tracking_error(excess_series):
    return excess_series.std()

def information_ratio(excess, tracking):
    return (excess.mean() * 252) / (tracking * (252 ** 0.5))

if __name__ == "__main__":
    df_asml = q_returns_indexed('ASML', '1y')
    df_spy = q_returns_indexed('SPY', '1y')

    rp = log_return(df_asml)
    rm = log_return(df_spy)

    excess = excess_return(rp, rm)
    print(excess)
    print()
    tracking = tracking_error(excess)
    print(tracking)
    print()
    info = information_ratio(excess, tracking)
    print(info)
