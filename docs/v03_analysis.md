## **v0.3 — Analysis | *First Sprout***

### **Overview**

Analysis layer that calculates performance ratios, correlation matrices and benchmarking metrics over the data stored in PostgreSQL. Builds on top of v0.2 feature engineering functions — particularly `log_return` from `returns.py`.

### **Data Flow**

```
PostgreSQL (stock\_prices)  
    ↓  
database/querys.py   → extracts adj\_close filtered by ticker and period  
    ↓  
ratios.py            → Sharpe, Sortino, Calmar, Beta, Alpha  
correlation.py       → returns and prices correlation matrix  
benchmarking.py      → excess return, tracking error, information ratio  
    ↑  
cli.py               → provides ticker and period from terminal
```
  
---

### **Modules**

#### **`ratios.py`**

Performance ratios module. Calculates industry-standard metrics to evaluate the risk-adjusted return of an asset.

**Design decision:** the risk-free rate `rf` is annualized using the compound interest formula `(1+rf)^(n/252)-1` where `n` is the number of days in the period. This is correct because compound interest reflects the real cost of time — linear scaling would be an incorrect approximation for long periods.

**Design decision:** `alpha_ratio` calls `beta_ratio` internally instead of receiving beta as a parameter. This guarantees consistency — alpha and beta are always calculated on the same series.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `sharpe_ratio(df, rf=0.05)` | `df: DataFrame`, `rf: float` | float — Sharpe ratio | Excess return per unit of total risk |
| `sortino_ratio(df, rf=0.05)` | `df: DataFrame`, `rf: float` | float — Sortino ratio | Excess return per unit of downside risk |
| `calmar_ratio(df)` | `df: DataFrame` | float — Calmar ratio | Return over maximum drawdown |
| `beta_ratio(df, benchmark)` | `df: DataFrame`, `benchmark: DataFrame` | float — beta | Asset sensitivity relative to benchmark |
| `alpha_ratio(df, benchmark, rf=0.05)` | `df: DataFrame`, `benchmark: DataFrame`, `rf: float` | float — alpha | Excess return relative to benchmark adjusted by beta |

**Note:** `sharpe_ratio` penalizes all volatility — both positive and negative. `sortino_ratio` only penalizes downside volatility, calculating standard deviation exclusively over negative returns. For assets with asymmetric returns, Sortino is more informative.

### **Usage**

python \-m analysis.ratios \<TICKER\> \<PERIOD\>

---

#### **`correlation.py`**

Correlation module. Measures the degree of joint movement between multiple assets, both over returns and over prices.

**Design decision:** the function receives a `{ticker: DataFrame}` dictionary instead of individual DataFrames, which allows calculating the correlation matrix for an arbitrary number of assets without changing the function signature.

**Design decision:** two versions are offered — over returns and over prices — because they have distinct interpretations. Return correlation measures dynamic co-movement period by period, which is what matters for portfolio construction. Price correlation can be spurious in non-stationary series.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `returns_correlation(assets)` | `assets: dict {ticker: DataFrame}` | DataFrame — correlation matrix over log returns | Portfolio construction, diversification analysis |
| `prices_correlation(assets)` | `assets: dict {ticker: DataFrame}` | DataFrame — correlation matrix over prices | Reference, use with caution on non-stationary series |

### **Usage**

python \-m analysis.correlation

---

#### **`benchmarking.py`**

Benchmarking module. Evaluates the performance of an asset relative to a benchmark through tracking metrics.

**Design decision:** functions are separated instead of being a single function that returns everything. This allows using each metric independently — for example, calculating only `tracking_error` without needing to calculate `information_ratio`.

**Design decision:** `information_ratio` annualizes both the mean excess return (×252) and the tracking error (×√252) to express the result on an annual scale, which is the industry standard.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `excess_return(rp, rm)` | `rp: Series`, `rm: Series` | Series — daily excess return | Base for tracking error and information ratio |
| `tracking_error(excess_series)` | `excess_series: Series` | float — tracking error | Volatility of excess return relative to benchmark |
| `information_ratio(excess, tracking)` | `excess: Series`, `tracking: float` | float — information ratio | Consistency of excess return per unit of tracking error |

### **Usage**

python \-m analysis.benchmarking  
