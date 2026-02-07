# CLAUDE.md

> AI assistant guide for the Options Analysis Toolkit

## Project Overview

A collection of Python-based financial analysis tools for stock options data, including options chain viewers and an implied volatility calculator using Black-Scholes pricing.

### What This Project Does
- Fetches current stock prices and options chains (NVDA, AAPL)
- Lists available options expiration dates
- Displays calls and puts near the money (±15% of current price)
- Calculates implied volatility using Black-Scholes model with Brent's method
- Provides `/iv` and `/iv-enhanced` skills for quick IV calculations from the CLI

## Codebase Structure

```
/
├── CLAUDE.md                          # This file - AI assistant guidelines
├── scripts/
│   ├── nvda_options.py                # NVDA options chain viewer
│   ├── aapl_options.py                # AAPL options chain viewer
│   └── options_vol_calculator.py      # IV calculator (Black-Scholes) - interactive & CLI modes
└── skills/
    ├── iv/
    │   └── SKILL.md                   # /iv slash command definition
    └── iv-enhanced/
        └── SKILL.md                   # /iv-enhanced skill (uses options_vol_calculator module)
```

### Key Files

**`scripts/nvda_options.py`** / **`scripts/aapl_options.py`** - Options chain viewers:
- Stock data retrieval via `yfinance.Ticker`
- Options chain fetching and filtering (±15% of current price)
- Formatted console output

**`scripts/options_vol_calculator.py`** - Implied volatility calculator:
- Black-Scholes pricing with dividend yield
- IV solving via `scipy.optimize.brentq`
- Fetches live underlying price from Yahoo Finance API
- Supports up to 3 option prices per calculation
- CLI mode: `python scripts/options_vol_calculator.py TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]`
- Interactive mode: `python scripts/options_vol_calculator.py` (no args)

**`skills/iv/SKILL.md`** - Claude Code skill for quick IV calculations:
- Usage: `/iv TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]`
- Example: `/iv AAPL 3/31/2026 300 call 1/31/2026 10 20`

**`skills/iv-enhanced/SKILL.md`** - Enhanced IV skill using the options_vol_calculator CLI:
- Runs `python scripts/options_vol_calculator.py` directly with arguments (fast, no AI code generation)
- Usage: `/iv-enhanced TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]`

## Dependencies

| Package | Purpose |
|---------|---------|
| `yfinance` | Yahoo Finance API wrapper for stock/options data |
| `pandas` | Data manipulation (implied by yfinance, used for DataFrames) |
| `scipy` | Brent's method for IV solving, normal distribution for Black-Scholes |

### Installation

```bash
pip install yfinance scipy
```

## Development Workflow

### Running Scripts

```bash
python scripts/nvda_options.py
python scripts/aapl_options.py
python scripts/options_vol_calculator.py
```

### Using the IV Skill

From Claude Code CLI, use the `/iv` or `/iv-enhanced` slash commands for quick calculations.

### Registering Skills

Skills live in two places:
- `skills/<name>/SKILL.md` — version-controlled source of truth in the repo
- `~/.claude/skills/<name>/SKILL.md` — where Claude Code discovers them

To register a new or updated skill, copy the file:
```bash
cp skills/<name>/SKILL.md ~/.claude/skills/<name>/SKILL.md
```
Don't use symlinks — they're unreliable on Windows. When updating a skill, update both copies.

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

## Testing Considerations

- **Network dependency**: Requires internet access to Yahoo Finance
- **Market hours**: Data freshness varies based on market status
- **Rate limiting**: Excessive requests may be throttled by Yahoo Finance

## Git Workflow

- **Always run `git pull` at the start of every session** before doing any work
- Branch naming: `claude/<description>-<session-id>`
- Commit messages should be descriptive of changes
- Push to feature branches, not directly to main

## Notes for AI Assistants

1. Keep scripts simple and self-contained
2. The yfinance API can change; check documentation if errors occur
3. Stock data is real-time during market hours, delayed otherwise
4. Options data structure depends on yfinance version
5. Always handle potential `None` values from API responses
6. The Yahoo Finance chart API (`query1.finance.yahoo.com`) is used as a lightweight alternative to yfinance for fetching just the current price
