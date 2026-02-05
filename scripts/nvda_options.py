import yfinance as yf

# Get NVDA stock
nvda = yf.Ticker("NVDA")

# Current stock price
print("=== NVDA Stock Price ===")
info = nvda.info
print(f"Current Price: ${info.get('currentPrice', 'N/A')}")
print(f"Previous Close: ${info.get('previousClose', 'N/A')}")
print()

# Get available expiration dates
print("=== Available Option Expiration Dates ===")
expirations = nvda.options
for exp in expirations[:10]:  # Show first 10
    print(exp)
print()

# Get options chain for nearest expiration
if expirations:
    nearest_exp = expirations[0]
    current_price = info.get('currentPrice', 180)

    print(f"=== Options Chain for {nearest_exp} ===")
    print(f"(Showing strikes near ${current_price})")

    opt_chain = nvda.option_chain(nearest_exp)

    # Filter strikes near current price (+/- 15%)
    low = current_price * 0.85
    high = current_price * 1.15

    calls_near = opt_chain.calls[(opt_chain.calls['strike'] >= low) & (opt_chain.calls['strike'] <= high)]
    puts_near = opt_chain.puts[(opt_chain.puts['strike'] >= low) & (opt_chain.puts['strike'] <= high)]

    print("\n-- CALLS (Near the Money) --")
    print(calls_near[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'impliedVolatility']].to_string(index=False))

    print("\n-- PUTS (Near the Money) --")
    print(puts_near[['strike', 'lastPrice', 'bid', 'ask', 'volume', 'impliedVolatility']].to_string(index=False))
