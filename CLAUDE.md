# CLAUDE.md

> AI assistant guide for the NVDA Options Analyzer repository

## Project Overview

This is a Python-based financial analysis tool that retrieves and displays NVIDIA (NVDA) stock options data using the Yahoo Finance API.

### What This Project Does
- Fetches current NVDA stock price information
- Lists available options expiration dates
- Displays options chains (calls and puts) near the current stock price
- Filters options within ±15% of the current price for relevance

## Codebase Structure

```
/
├── nvda_options.py    # Main script for fetching and displaying options data
├── CLAUDE.md          # This file - AI assistant guidelines
└── .git/              # Git repository
```

### Key File

**`nvda_options.py`** - Single-file script containing all functionality:
- Stock data retrieval via `yfinance.Ticker`
- Options chain fetching and filtering
- Formatted console output

## Dependencies

| Package | Purpose |
|---------|---------|
| `yfinance` | Yahoo Finance API wrapper for stock/options data |
| `pandas` | Data manipulation (implied by yfinance, used for DataFrames) |

### Installation

```bash
pip install yfinance
```

## Development Workflow

### Running the Script

```bash
python nvda_options.py
```

### Expected Output
1. Current NVDA stock price and previous close
2. First 10 available options expiration dates
3. Calls and puts near the money for the nearest expiration

## Code Conventions

### Style Guidelines
- Use descriptive variable names (e.g., `nearest_exp`, `current_price`)
- Include section headers with `===` formatting for console output
- Filter large datasets to show only relevant information
- Use f-strings for string formatting

### Data Handling
- Always use `.get()` with fallback values when accessing dict keys
- Filter DataFrames using boolean indexing
- Display relevant columns only (strike, lastPrice, bid, ask, volume, impliedVolatility)

## Common Tasks for AI Assistants

### Adding New Stock Symbols
To analyze a different stock, modify the ticker symbol:
```python
stock = yf.Ticker("SYMBOL")
```

### Adjusting Price Range Filter
The ±15% filter can be modified in lines 31-32:
```python
low = current_price * 0.85   # -15%
high = current_price * 1.15  # +15%
```

### Adding New Data Fields
Options chain DataFrames include additional columns:
- `openInterest`, `inTheMoney`, `contractSize`, `currency`, `lastTradeDate`

## Testing Considerations

- **Network dependency**: Requires internet access to Yahoo Finance
- **Market hours**: Data freshness varies based on market status
- **Rate limiting**: Excessive requests may be throttled by Yahoo Finance

## Git Workflow

- Branch naming: `claude/<description>-<session-id>`
- Commit messages should be descriptive of changes
- Push to feature branches, not directly to main

## Notes for AI Assistants

1. This is a single-file project - keep it simple
2. The yfinance API can change; check documentation if errors occur
3. Stock data is real-time during market hours, delayed otherwise
4. Options data structure depends on yfinance version
5. Always handle potential `None` values from API responses
