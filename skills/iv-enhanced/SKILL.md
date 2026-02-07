---
name: iv-enhanced
description: Calculate implied volatility using the options_vol_calculator module
argument-hint: "TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]"
---

Calculate implied volatility using the existing options_vol_calculator.py module.

Parse the arguments: $ARGUMENTS

Expected format: TICKER EXP_DATE STRIKE TYPE VAL_DATE PRICE_A [PRICE_B] [PRICE_C]

Example: AAPL 3/31/2026 300 call 1/31/2026 10 20

Steps:
1. Parse expiration date and valuation date (accept M/D/YYYY or YYYY-MM-DD, normalize to YYYY-MM-DD)
2. Import functions from `scripts/options_vol_calculator.py` using Python
3. Fetch the live stock price by calling the same Yahoo Finance approach used in the script's `main()` function (urllib with query1.finance.yahoo.com)
4. Use risk-free rate r=0.045 (4.5%)
5. Estimate dividend yield (0 for non-dividend stocks, ~0.005 for dividend payers)
6. Call `calculate_time_to_expiry(val_date, exp_date)` from the module to get T
7. For each option price provided, call `implied_volatility(price, S, K, T, r, q, option_type)` from the module
8. Display results in a clean table showing: underlying price, strike, type, dates, and each price with its corresponding IV

Run the calculation using `python -c` with `sys.path` adjusted to import from the `scripts/` directory:
```
import sys; sys.path.insert(0, 'scripts')
from options_vol_calculator import implied_volatility, calculate_time_to_expiry, format_vol
```
