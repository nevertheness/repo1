# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Options Analysis Toolkit — Python CLI tools for stock options data. Fetches options chains via yfinance, displays near-the-money calls/puts, and calculates implied volatility using Black-Scholes with Brent's method.

## Commands

```bash
# Install dependencies
pip install yfinance scipy

# Run options chain viewers
python scripts/nvda_options.py
python scripts/aapl_options.py

# IV calculator - interactive mode
python scripts/options_vol_calculator.py

# IV calculator - CLI mode (supports up to 3 prices)
python scripts/options_vol_calculator.py TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]
# Example: python scripts/options_vol_calculator.py AAPL 3/31/2026 300 call 1/31/2026 10 20
```

No test suite, linter, or build step exists. Scripts are run directly.

## Architecture

- **`scripts/nvda_options.py`** / **`scripts/aapl_options.py`** — Standalone options chain viewers using `yfinance.Ticker`. Filter to ±15% of current price. Nearly identical; only the ticker symbol differs.
- **`scripts/options_vol_calculator.py`** — IV calculator with two modes (interactive and CLI). Uses `scipy.optimize.brentq` for solving and the Yahoo Finance chart API (`query1.finance.yahoo.com`) as a lightweight price source instead of yfinance. Supports dividend yield in Black-Scholes pricing.
- **`skills/iv/SKILL.md`** — `/iv` slash command: directly invokes `options_vol_calculator.py` CLI.

Skills must be copied to `~/.claude/skills/<name>/SKILL.md` for Claude Code to discover them. Don't use symlinks.

## Dependencies

`yfinance` (options chain data), `scipy` (Brent's method + normal distribution for Black-Scholes), `pandas` (implicit via yfinance).

## Code Conventions

- Descriptive variable names (e.g., `nearest_exp`, `current_price`)
- Console section headers with `===` formatting
- Use `.get()` with fallback values on dict keys from API responses
- Filter DataFrames with boolean indexing; display only: strike, lastPrice, bid, ask, volume, impliedVolatility
- f-strings for formatting
- Handle potential `None` values from Yahoo Finance API responses

## Git Workflow

- **Always run `git pull` at the start of every session** before doing any work
- Branch naming: `claude/<description>-<session-id>`
- Push to feature branches, not directly to main

## Notes

- Network access to Yahoo Finance required for all scripts
- Data freshness varies with market hours; rate limiting possible
- The yfinance API can change across versions; check docs if errors occur
- The Yahoo Finance chart API is used in `options_vol_calculator.py` as a lightweight alternative to the full yfinance library for fetching current price only
