---
name: iv
description: Calculate implied volatility for options using Black-Scholes
argument-hint: "TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]"
---

Calculate implied volatility using the Black-Scholes model.

Parse the arguments: $ARGUMENTS

Expected format: TICKER EXP_DATE STRIKE TYPE VAL_DATE PRICE_A [PRICE_B] [PRICE_C]

Example: AAPL 3/31/2026 300 call 1/31/2026 10 20

Steps:
1. Fetch the live stock price from Yahoo Finance using urllib
2. Use risk-free rate r=0.045 (4.5%)
3. Estimate dividend yield (0 for non-dividend stocks, ~0.005 for dividend payers)
4. Parse expiration date and valuation date (accept M/D/YYYY or YYYY-MM-DD)
5. Calculate time to expiry T in years
6. For each option price provided, calculate implied volatility using Brent's method on the Black-Scholes formula
7. Display results in a clean table showing: underlying price, strike, type, dates, and each price with its corresponding IV

Use scipy.stats.norm and scipy.optimize.brentq. Run the calculation inline with python -c.
