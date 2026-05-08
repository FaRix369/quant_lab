# QUANT_LAB
*From the pocket to the world. A personal quantitative finance laboratory — built version by version, layer by layer.*

---

### Roadmap

This project is built on systems thinking and systems theory — each version is a layer that builds on the previous one, forming a system that grows in complexity and capability organically. Every design decision reflects a systemic perspective: separation of responsibilities, modularity, emergent behavior from simple components, and feedback between layers. The end goal is not just a collection of tools, but a system that thinks.

- **v0.1 — Planting the Seed** — ETL pipeline: extraction, transformation, load ✅
- **v0.2 — Taking Root** — Feature engineering: returns, volatility, drawdown, z-score ✅
- **v0.3 — First Sprout** — Analysis: performance ratios, correlation, benchmarking ✅
- **v0.4 — ?** — Visualization
- **v0.5 — ?** — Backtesting engine (C++/Rust)
- **v0.6 — ?** — Machine learning integration
- **v0.7 — ?** — Simulations: Monte Carlo, GBM, agent-based models

Cross-cutting layers across all versions: data validation, logging, config, multi-asset support.

**End goal:** a complete quantitative laboratory, comparable in structure to the research environments of investment funds.

---


### Data

Data is the foundation of every analysis, every decision. It is data that moves the world and the agents within it. The starting point of every decision, every movement, every impulse, lies in data — and in the information we build from it.

Every system — financial, natural, social — feeds on information to operate. QUANT_LAB starts at the beginning: collection, transformation, storage — and grows from there into analysis, visualization, and simulation.

---

### Architecture

```
yfinance API
↓
pipelines/stock_collector/     (v0.1)
api_client.py   → extracts raw OHLCV + Adj Close
transform.py    → normalizes, renames, adds ticker
db_writer.py    → inserts into PostgreSQL
collector.py    → orchestrates the pipeline
↓
PostgreSQL (stock_prices)
↓
feature_engineering/           (v0.2)
returns.py      → log, simple, arithmetic returns
rolling.py      → rolling mean, std, min, max
volatility.py   → historic, annualized, rolling, EWMA
drawdown.py     → drawdown, duration, recovery
zscore.py       → historic and mobile z-score
↓
analysis/                      (v0.3)
ratios.py       → Sharpe, Sortino, Calmar, Beta, Alpha
correlation.py  → returns and prices correlation matrix
benchmarking.py → excess return, tracking error, information ratio
Cross-cutting: database/ (connection + queries) · cli/ (argument handling)
```

---

### Security

Database credentials are managed via environment variables. The `.env` file is never committed to the repository — it is listed in `.gitignore`. A `.env.example` template is provided.

---

### Stack

- Python 3.12
- yfinance
- pandas
- numpy
- psycopg2
- SQLAlchemy
- python-dotenv
- PostgreSQL

---

### Installation

```bash
git clone <repo-url>
cd quant_lab
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## v0.1 — Stock Collector | *Planting the Seed*

*Selection, collection, and storage. Every system starts with data.*

The pipeline extracts historical stock price data from Yahoo Finance, transforms it into a normalized format, and loads it into a PostgreSQL database.

| Module | Role |
|---|---|
| `api_client.py` | Queries yfinance. Handles connection errors and timeouts. Returns OHLCV + Adj Close. |
| `transform.py` | Drops redundant columns, adds ticker, normalizes datetime index, renames to snake_case. |
| `db_writer.py` | Inserts into PostgreSQL as an atomic transaction. Handles duplicates with `ON CONFLICT DO NOTHING`. |
| `collector.py` | Orchestrator. Connects the three modules in sequence. |

**Usage:**
```bash
python -m pipelines.stock_collector.collector <TICKER> <PERIOD>
```
```bash
python -m pipelines.stock_collector.collector ASML 1y
```

Valid periods: `1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max`

---

## v0.2 — Feature Engineering | *Taking Root*

*Raw metrics gain meaning. The system starts to understand what it holds.*

Calculates financial metrics over the adjusted close price series stored in PostgreSQL. Each module is independent and can be used directly from the terminal.

| Module | Role |
|---|---|
| `returns.py` | Log, simple and arithmetic returns — daily and cumulative. |
| `rolling.py` | Rolling mean, std, min and max over a configurable window. |
| `volatility.py` | Historic, annualized, rolling and EWMA volatility over log returns. |
| `drawdown.py` | Daily drawdown, max drawdown, peak, trough, duration and recovery time. |
| `zscore.py` | Historic and mobile z-score over log returns. |

**Usage:**
```bash
python -m feature_engineering.<module> <TICKER> <PERIOD> <WINDOW>
```
```bash
python -m feature_engineering.volatility ASML 1y 20
```

---

## v0.3 — Analysis | *First Sprout*

*Comparison becomes possible. The system can now evaluate and measure.*

Calculates performance ratios, correlation matrices and benchmarking metrics. Builds on top of v0.2 feature engineering functions.

| Module | Role |
|---|---|
| `ratios.py` | Sharpe, Sortino, Calmar, Beta and Alpha ratios. |
| `correlation.py` | Returns and prices correlation matrix for multiple assets. |
| `benchmarking.py` | Excess return, tracking error and information ratio relative to a benchmark. |

**Usage:**
```bash
python -m analysis.ratios <TICKER> <PERIOD>
```
```bash
python -m analysis.ratios ASML 1y
```

---

*QUANT_LAB, 2026*
