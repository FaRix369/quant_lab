import matplotlib
import matplotlib.pyplot as plt
from database.querys import q_price_chart
matplotlib.use('TkAgg')
from matplotlib.ticker import EngFormatter

def close_price(date, close, adj_close):
    fig, ax = plt.subplots()
    ax.plot(date, close, label='Close Price')
    ax.plot(date, adj_close, label='Adj Close Price')
    ax.legend()
    ax.set_title('Closes Prices')
    ax.set_xlabel('Date (days)')
    ax.set_ylabel('Prices')
    plt.show()
    return fig

def volume_chart(date, volume):
    fig, ax = plt.subplots()
    ax.bar(date, volume, label='Volume')
    ax.yaxis.set_major_formatter(EngFormatter())
    ax.legend()
    ax.set_title('Volume')
    ax.set_xlabel('Date (days)')
    ax.set_ylabel('Volume')
    plt.show()
    return fig

if __name__ == "__main__":
    df_asml = q_price_chart('ASML', '6mo')
    date = df_asml.index
    close = df_asml['close']
    adj = df_asml['adj_close']
    volume = df_asml['volume']

    cl = close_price(date, close, adj)
    vol = volume_chart(date, volume)
