import matplotlib
from pipelines.stock_collector.collector import collect
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
import numpy as np

def close_price(date, close, adj_close):
    fig, ax = plt.subplots()
    ax.plot(date, close, label='Close Price')
    ax.plot(date, adj_close, label='Adj Close Price')
    ax.legend()
    ax.set_title("Closes Prices")
    ax.set_xlabel('Date (days)')
    ax.set_ylabel('Prices')
    plt.show()
    return fig


if __name__ == "__main__":
    df_asml = collect('ASML', '1y')
    date = df_asml['date']
    close = df_asml['close']
    adj = df_asml['adj_close']
    print(df_asml)

    cl = close_price(date, close, adj)
