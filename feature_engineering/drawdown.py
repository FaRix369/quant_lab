from database.querys import q_returns

def function_drawdown(df):       #drawdown day by day
    adj_close = df['adj_close']
    max = adj_close.cummax()
    drawdown =  (adj_close - max)/max
    return drawdown

def max_drawdown(drawdown):
    max_drop = drawdown.min()
    return max_drop

def peak_price(df):
    adj_close = df['adj_close']
    peak = adj_close.cummax().max()
    return peak

def trough_price(df):
    adj_close = df['adj_close']
    trough = adj_close.min()
    return trough

def drawdown_duration(drawdown):
    count_day = 0
    max_duration = 0
    for i in drawdown:
        if i < 0:
            count_day += 1
            if count_day > max_duration:
                max_duration = count_day
        elif i >= 0:
            count_day = 0
    return max_duration

def recovery_time(drawdown):
    recovery = 0
    idx_trough = drawdown.idxmin()
    drawdown_from_trough = drawdown[idx_trough:]
    for i in drawdown_from_trough:
        if i < 0:
            recovery += 1
        elif i >= 0:
            break
    return recovery