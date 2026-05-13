from matplotlib.ticker import PercentFormatter
from feature_engineering.returns import log_return
from feature_engineering.volatility import rolling_volatility
import matplotlib
from database.querys import q_price_chart
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def returns_chart(date, returns):
    colors = ['green' if r > 0 else 'red' for r in returns]
    fig, ax = plt.subplots()
    ax.bar(date, returns, label='Returns', color=colors)
    ax.legend()
    ax.set_title('Returns')
    ax.set_xlabel('Date (days)')
    ax.set_ylabel('Returns')
    plt.show()
    return fig

def volatility_chart(date, volatility):
    fig, ax = plt.subplots()
    ax.plot(date, volatility, label='Volatility Price')
    ax.yaxis.set_major_formatter(PercentFormatter(xmax=1))
    ax.legend()
    ax.set_title('Volatility')
    ax.set_xlabel('Date')
    ax.set_ylabel('Volatility')
    plt.show()
    return fig

if __name__ == "__main__":
    df_asml = q_price_chart('ASML', '6mo')
    date = df_asml.index
    volume = df_asml['volume']
    returns = log_return(df_asml)
    volatility = rolling_volatility(returns, 20)

    returns_c = returns_chart(date, returns)
    volatility_c = volatility_chart(date, volatility)