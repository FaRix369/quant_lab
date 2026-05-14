## **v0.4 — Visualization | First Leaves** 

### **Overview**

Visualization layer that generates charts from data stored in PostgreSQL. Each module covers a specific category of charts — prices, feature engineering metrics, and analysis results. All charts use matplotlib with the TkAgg backend for rendering in desktop environments.

**System requirement:** `python3-tk` must be installed at system level for TkAgg to work:

bash  
sudo apt install python3-tk

### **Data Flow**

PostgreSQL (stock\_prices)  
    ↓  
database/querys.py      → q\_price\_chart() for price/volume/feature charts  
                                     → q\_returns\_indexed() for analysis charts  
    ↓  
visualization/  
    price\_charts.py         → close price, volume  
    feature\_charts.py      → returns, rolling volatility  
    analysis\_chart.py      → correlation scatter, benchmarking  
    ↑  
cli.py                             → not used in v0.4 — data hardcoded in \_\_main\_\_

### **Usage**

All scripts are run as modules from the project root with `pip install -e .` active:

*python \-m visualization.price\_charts*  
*python \-m visualization.feature\_charts*  
*python \-m visualization.analysis\_chart*  
---

### **Modules**

#### **`price_charts.py`**

Price and volume visualization module. Plots raw price series and trading volume directly from the DB.

| Function | Receives | Returns | Use |
| ----- | ----- | ----- | ----- |
| `close_price(date, close, adj_close)` | `date: Index`, `close: Series`, `adj_close: Series` | matplotlib figure | Compares raw close and adjusted close price over time |
| `volume_chart(date, volume)` | `date: Index`, `volume: Series` | matplotlib figure | Trading volume over time. Y-axis formatted with `EngFormatter` for readability |

---

#### **`feature_charts.py`**

Feature engineering visualization module. Plots log returns and rolling volatility over the adjusted close price series.

**Note:** `rolling_volatility` uses `window=20` (trading days, \~1 month). The first 19 values are NaN due to insufficient prior data — the chart shows volatility evolution over the full period starting from day 20\.

| Function | Receives | Returns | Use |
| ----- | ----- | ----- | ----- |
| `returns_chart(date, returns)` | `date: Index`, `returns: Series` | matplotlib figure | Daily log returns as bar chart. Green for positive, red for negative |
| `volatility_chart(date, volatility)` | `date: Index`, `volatility: Series` | matplotlib figure | Rolling volatility over time. Y-axis formatted as percentage |

---

#### **`analysis_chart.py`**

Analysis visualization module. Plots correlation and benchmarking metrics calculated in v0.3.

| Function | Receives | Returns | Use |
| ----- | ----- | ----- | ----- |
| `correlation_scatter(asset1, asset2, label1, label2)` | `asset1: Series`, `asset2: Series`, `label1: str`, `label2: str` | matplotlib figure | Scatter plot of log returns between two assets with regression line and correlation coefficient |
| `benchmarking_chart(date, excess)` | `date: Index`, `excess: Series` | matplotlib figure | Daily excess return vs benchmark as bar chart. Green for outperformance, red for underperformance |

