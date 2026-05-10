## **v0.2 — Feature Engineering | *Taking Root***

### **Overview**

Feature engineering layer that calculates financial metrics over the adjusted close price series stored in PostgreSQL. Each module is independent and can be used directly from the terminal or imported by other modules.

### **Data Flow**
```
PostgreSQL (stock\_prices)  
    ↓  
database/querys.py  → extracts adj\_close filtered by ticker and period  
    ↓  
returns.py        → log, simple, arithmetic returns  
rolling.py        → rolling mean, std, min, max  
volatility.py     → historic, annualized, rolling, EWMA volatility  
drawdown.py       → drawdown, duration, recovery  
zscore.py         → historic and mobile z-score  
    ↑  
cli.py            → provides ticker, period and window from terminal
```
  
---

### **Modules**

#### **`returns.py`**

Returns module. Calculates different types of financial return over the adjusted price series extracted from the DB.

**Design decision:** all calculations work on `adj_close` and not on `close` because the adjusted price reflects the real investor return, incorporating dividends and splits. Using raw `close` would generate false signals at points where those events occurred.

**Design decision:** log returns are preferred over arithmetic ones for time series analysis because they are additive across time — they can be summed directly across periods. Arithmetic returns are useful for intuitive interpretation of point-in-time results.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `log_return(df)` | `df: DataFrame` | Series — daily log return | Base for volatility and z-score |
| `log_return_digit(df)` | `df: DataFrame` | float — cumulative log return | Total return of the period in logarithmic scale |
| `simple_return(df)` | `df: DataFrame` | float — cumulative simple return | Total return of the period in natural scale |
| `aritmetic_return(df)` | `df: DataFrame` | Series — daily arithmetic return | Day-to-day percentage change |
| `aritmetic_return_digit(df)` | `df: DataFrame` | float — cumulative arithmetic return | Total compounded return of the period |

### **Usage**

**python \-m feature\_engineering.returns \<TICKER\> \<PERIOD\>**

---

#### **`rolling.py`**

Rolling statistics module. Provides base functions consumed both directly and by other feature engineering modules.

**Design decision:** `rolling_mean`, `rolling_std`, `rolling_min` and `rolling_max` accept both DataFrame and Series as input via `isinstance(pd.DataFrame)`. This allows `zscore.py` to pass a log returns Series directly without prior conversion.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `rolling_mean(df, window)` | `df: DataFrame or Series`, `window: int` | Series — rolling mean | Used internally by `zscore.py` |
| `rolling_std(df, window)` | `df: DataFrame or Series`, `window: int` | Series — rolling std | Used internally by `zscore.py` |
| `rolling_min(df, window)` | `df: DataFrame or Series`, `window: int` | Series — rolling min | Range analysis by window |
| `rolling_max(df, window)` | `df: DataFrame or Series`, `window: int` | Series — rolling max | Range analysis by window |

### **Usage**

**python \-m feature\_engineering.rolling \<TICKER\> \<PERIOD\> \<WINDOW\>**


---

#### **`volatility.py`**

Volatility module. Calculates different dispersion measures of the logarithmic return, each with a distinct analytical purpose.

**Design decision:** all functions receive the log returns Series as input instead of the original DataFrame. This separates responsibility — `returns.py` calculates the returns, `volatility.py` analyzes them. The module does not access the DB directly.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `historic_simple_volatility(return_log)` | `return_log: Series` | float — daily historic volatility | Base for annualized volatility |
| `anualized_volatility(hs_volatility)` | `hs_volatility: float` | float — annualized volatility | Scales daily volatility to 252 trading days |
| `rolling_volatility(return_log, window)` | `return_log: Series`, `window: int` | Series — rolling volatility | Evolution of volatility over time |
| `ewma_volatility(return_log, lam=0.94)` | `return_log: Series`, `lam: float` | Series — EWMA volatility | Volatility with higher weight on recent observations |

**Note:** the factor 252 represents trading days in a year. λ=0.94 is the RiskMetrics standard for daily assets.

### **Usage**

**python \-m feature\_engineering.volatility \<TICKER\> \<PERIOD\> \<WINDOW\>**

---

#### **`drawdown.py`**

Drawdown module. Measures price decline from historical highs and quantifies the duration and recovery of those declines.

**Design decision:** all functions work on `adj_close` to reflect the real impact on investor capital including dividends and splits.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `function_drawdown(df)` | `df: DataFrame` | Series — daily drawdown | Base for the rest of the module's functions |
| `max_drawdown(drawdown)` | `drawdown: Series` | float — maximum decline | Worst loss from a peak in the period |
| `peak_price(df)` | `df: DataFrame` | float — historical peak price | Highest point reached in the period |
| `trough_price(df)` | `df: DataFrame` | float — absolute minimum price | Lowest point reached in the period |
| `drawdown_duration(drawdown)` | `drawdown: Series` | int — days | Longest continuous streak in negative territory |
| `recovery_time(drawdown)` | `drawdown: Series` | int — days | Days from trough until recovering neutral ground |

### **Usage**

**python \-m feature\_engineering.drawdown \<TICKER\> \<PERIOD\> \<WINDOW\>**

---

#### **`zscore.py`**

Z-score module. Standardizes log returns to identify statistically atypical values relative to the historical distribution or a rolling window.

**Design decision:** z-score is applied on log returns and not on raw prices because returns are stationary — they have stable mean and variance over time. Applying z-score on prices would produce statistically meaningless results.

**Internal dependencies:** both functions import `log_return` from `returns.py`. `z_score_mobile` also uses `rolling_mean` and `rolling_std` from `rolling.py`.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `z_score_historic(df)` | `df: DataFrame` | Series — historic z-score | Anomalies relative to the full period distribution |
| `z_score_mobile(df, window)` | `df: DataFrame`, `window: int` | Series — mobile z-score | Anomalies relative to a recent window |

### 

### **Usage**

**python \-m feature\_engineering.zscore \<TICKER\> \<PERIOD\> \<WINDOW\>** 
