## **QUANT\_LAB — Architecture**

### **Overview**

QUANT\_LAB is a personal quantitative finance laboratory structured as a modular, versioned system. Each version adds a functional layer on top of the previous one, following strict separation of responsibilities.

The project is organized in four layers:

| Layer | Folder | Role |
| :---- | :---- | :---- |
| DB Infrastructure | `database/` | Reusable connection and queries |
| CLI Interface | `cli/` | Terminal argument handling |
| Pipelines | `pipelines/` | ETL: extraction, transformation, load |
| Feature Engineering | `feature_engineering/` | Financial metrics over DB data |
| Analysis | `analysis/` | Performance ratios, correlation, benchmarking |

`database/` and `cli/` are cross-cutting modules — they belong to no specific version and serve the entire system.

---

### **System Data Flow**

```

yfinance API  
    ↓  
pipelines/stock\_collector/    (v0.1)  
    api\_client.py   → extracts raw DataFrame (OHLCV \+ Adj Close)  
    transform.py    → normalizes, renames, adds ticker  
    db\_writer.py    → inserts into PostgreSQL (stock\_prices)  
    collector.py    → orchestrates the three modules above  
    ↑  
cli/cli.py          → provides ticker and period from terminal

PostgreSQL (stock\_prices)  
    ↓  
database/querys.py  → extracts adj\_close filtered by ticker and period  
    ↓  
feature\_engineering/          (v0.2)  
    returns.py      → log, simple, arithmetic returns  
    rolling.py      → rolling mean, std, min, max  
    volatility.py   → historic, annualized, rolling, EWMA volatility  
    drawdown.py     → drawdown, duration, recovery  
    zscore.py       → historic and mobile z-score  
    ↓  
analysis/                     (v0.3)  
    ratios.py       → Sharpe, Sortino, Calmar, Beta, Alpha  
    correlation.py  → returns and prices correlation matrix  
    benchmarking.py → excess return, tracking error, information ratio  
    ↑  
cli/cli.py          → provides ticker, period and window from terminal  
```


### **Cross-cutting Modules**

#### **`database/db_connection.py`**

Centralizes all PostgreSQL connection logic. The only point in the project that reads credentials from `.env` and uses them to create connections. No other module accesses credentials directly.

**Design decision:** credentials are never hardcoded. They are read from a `.env` file that is never committed to the repository. The path to `.env` is resolved dynamically using chained `os.path` calls from the file's own location, which guarantees it works regardless of where the project is executed from.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `connection_database()` | — | psycopg2 connection | Write operations (INSERT, commit, rollback) |
| `get_engine()` | — | SQLAlchemy engine | Read operations with pandas (`read_sql`) |

---

#### **`database/querys.py`**

Centralizes reusable SQL queries. Each function represents a specific query that can be called from any module across the system. `PERIOD_MAP` is defined at module level and shared by all functions.

**Design decision:** queries are separated from analysis code to maintain separation between data access and business logic. If the DB schema changes, only this file needs to be modified.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `q_returns(ticker, period)` | `ticker: str`, `period: str` | DataFrame with `adj_close` column | Base for all feature engineering calculations |
| `q_returns_indexed(ticker, period)` | `ticker: str`, `period: str` | DataFrame with `date` as index and `adj_close` column | Base for calculations requiring temporal alignment between assets |

**Design decision:** `q_returns_indexed` returns the DataFrame with `date` as index, ordered chronologically. This is required for alignment operations between assets in `beta_ratio`, `correlation` and `benchmarking`, where pandas needs the temporal index to correctly align observations.

---

#### **`cli/cli.py`**

Encapsulates all command-line argument logic. Modules that need arguments import a function from here instead of defining their own `argparse`.

**Design decision:** centralizing the CLI prevents each module from defining its own parser, which would cause involuntary execution on import. All entry points in the project use these functions inside the `if __name__ == '__main__'` block.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `get_ticker_period()` | — | `(ticker, period)` | v0.1 collector, v0.2 returns |
| `get_window()` | — | `(ticker, period, window)` | v0.2 rolling, volatility, drawdown, zscore |

