---
name: iv-enhanced
description: Calculate implied volatility using the options_vol_calculator module
argument-hint: "TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]"
---

Calculate implied volatility using the options_vol_calculator.py CLI mode.

Arguments: $ARGUMENTS

Simply run this command from the repo root:

```bash
python scripts/options_vol_calculator.py $ARGUMENTS
```

The script accepts dates in M/D/YYYY or YYYY-MM-DD format and fetches the live underlying price automatically.
