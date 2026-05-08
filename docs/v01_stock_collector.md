## **v0.1 — Stock Collector | *Planting the Seed***

### **Overview**

ETL pipeline that extracts historical stock price data from Yahoo Finance via `yfinance`, transforms it into a normalized format, and loads it into a PostgreSQL database.

### **Data Flow**

yfinance API  
    ↓  
api\_client.py   → extracts raw DataFrame (OHLCV \+ Adj Close)  
    ↓  
transform.py    → normalizes, renames, adds ticker  
    ↓  
db\_writer.py    → inserts into PostgreSQL (stock\_prices)  
    ↑  
collector.py    → orchestrates the three modules above  
    ↑  
cli.py          → provides ticker and period from terminal

### **Database Schema**

CREATE TABLE stock\_prices (  
    id            SERIAL PRIMARY KEY,  
    ticker       TEXT NOT NULL,  
    date         DATE NOT NULL,  
    open        NUMERIC,  
    high         NUMERIC,  
    low           NUMERIC,  
    close        NUMERIC,  
    adj\_close  NUMERIC,  
    volume      BIGINT  
);

ALTER TABLE stock\_prices  
ADD CONSTRAINT unique\_ticker\_date UNIQUE (ticker, date);  
---

### **Modules**

#### **`api_client.py`**

Extraction module. The only point in the project that communicates with the yfinance API. Returns a raw DataFrame ready to be transformed.

**Design decision:** `auto_adjust=False` is used explicitly to obtain both `Close` and `Adj Close` as separate columns. The adjusted price incorporates dividends and splits — essential for correct return calculations in quant finance. Using `auto_adjust=True` would hide this distinction.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `history_price(name, period)` | `name: str`, `period: str` | Raw yfinance DataFrame or `None` | First step of the ETL |

**Error handling:** validates the period before calling the API. Catches connection errors, timeouts, and any general exception. Returns `None` if the DataFrame is empty.

---

#### **`transform.py`**

Transformation module. Takes the raw yfinance DataFrame and converts it to the exact format expected by the `stock_prices` table in PostgreSQL.

**Design decision:** the transform acts as a bridge between the DataFrame world and the DB contract. If the data source changes, only this module needs to be modified — the DB does not depend on yfinance's column names.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `transform_data(df, ticker)` | `df: DataFrame`, `ticker: str` | Normalized DataFrame | Second step of the ETL |

**Operations in order:**

1. Drops `Dividends` and `Stock Splits` columns — redundant since `Adj Close` already incorporates those events  
2. Adds `ticker` column — not present in the yfinance DataFrame  
3. Normalizes the index — removes time and timezone from `DatetimeTZDtype`  
4. Converts index to column with `reset_index()`  
5. Renames columns to `snake_case` to match the SQL schema

---

#### **`db_writer.py`**

Load module. Inserts the transformed DataFrame into the `stock_prices` table as an atomic transaction.

**Design decision:** `ON CONFLICT DO NOTHING` handles duplicates at the DB level using the `UNIQUE (ticker, date)` constraint. If a record already exists, it is silently ignored without failing. The rollback guarantees that an error mid-insertion does not leave partial data.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `writer(df)` | `df: DataFrame` | — | Third step of the ETL |

**Transaction flow:**

1. Opens connection and cursor  
2. Iterates rows and inserts with `ON CONFLICT DO NOTHING`  
3. `commit()` if everything succeeded  
4. `rollback()` if an error occurred  
5. `finally` closes cursor and connection always

---

#### **`collector.py`**

ETL pipeline orchestrator. Contains no logic of its own — its only role is to connect the three modules above in sequence.

| Function | Receives | Returns | Use |
| :---- | :---- | :---- | :---- |
| `collect(ticker, period)` | `ticker: str`, `period: str` | — | Complete ETL entry point |

### 

### **Usage**

***python \-m pipelines.stock\_collector.collector \<TICKER\> \<PERIOD\>***

Example:

**python \-m pipelines.stock\_collector.collector ASML 1y**

**Valid periods:** `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`

