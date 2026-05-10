from feature_engineering.returns import log_return
from pipelines.stock_collector.collector import collect
import matplotlib
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

if __name__ == "__main__":
    df_asml = collect('ASML', '6mo')
    date = df_asml['date']
    volume = df_asml['volume']
    returns = log_return(df_asml)

    retu = returns_chart(date, returns)