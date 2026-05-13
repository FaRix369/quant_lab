import matplotlib
import numpy as np
import pandas as pd
from analysis.benchmarking import excess_return
from feature_engineering.returns import log_return
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from database.querys import q_returns_indexed

def correlation_scatter(asset1, asset2, label1, label2):
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(asset1, asset2, alpha=0.6)
    m, b = np.polyfit(asset1, asset2, 1)
    ax.plot(asset1, m * asset1 + b)
    ax.set_xlabel(label1)
    ax.set_ylabel(label2)
    corr = np.corrcoef(asset1, asset2)[0, 1]
    ax.set_title(f'Correlation: {corr:.2f}')
    plt.show()
    return fig

def benchmarking_chart(date, excess):
    colors = ['green' if r > 0 else 'red' for r in excess]
    fig, ax = plt.subplots()
    ax.bar(date, excess, label='Excess Returns', color=colors)
    ax.legend()
    ax.set_title('Excess Return vs Benchmark')
    ax.set_xlabel('Date (days)')
    ax.set_ylabel('Excess Returns')
    plt.show()
    return fig    

if __name__ == "__main__":
    asml = q_returns_indexed('ASML', '1y')
    spy = q_returns_indexed('SPY', '1y')

    asml_returns = log_return(asml)
    spy_returns = log_return(spy)

    excess = excess_return(asml_returns, spy_returns)

    excess = excess.dropna()
    date = excess.index #use excess index to ensure date alignment

    returns = pd.concat([asml_returns, spy_returns],axis=1).dropna()

    correlation_scatter(returns.iloc[:, 0], returns.iloc[:, 1], 'ASML', 'SPY')

    bench_chart = benchmarking_chart(date, excess)

"python -m visualization.analysis_chart"

