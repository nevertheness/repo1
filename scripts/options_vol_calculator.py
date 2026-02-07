import math
from scipy.stats import norm
from scipy.optimize import brentq
from datetime import datetime
import urllib.request
import json


def black_scholes_price(S, K, T, r, q, sigma, option_type='call'):
    """
    Calculate Black-Scholes option price with dividend yield.

    S: Current stock price
    K: Strike price
    T: Time to expiration (in years)
    r: Risk-free rate (annual)
    q: Dividend yield (annual)
    sigma: Volatility (annual)
    option_type: 'call' or 'put'
    """
    if T <= 0:
        if option_type == 'call':
            return max(S - K, 0)
        else:
            return max(K - S, 0)

    d1 = (math.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    if option_type == 'call':
        price = S * math.exp(-q * T) * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    else:
        price = K * math.exp(-r * T) * norm.cdf(-d2) - S * math.exp(-q * T) * norm.cdf(-d1)

    return price


def implied_volatility(option_price, S, K, T, r, q, option_type='call'):
    """
    Calculate implied volatility using Brent's method.
    """
    def objective(sigma):
        return black_scholes_price(S, K, T, r, q, sigma, option_type) - option_price

    try:
        iv = brentq(objective, 0.001, 10.0)
        return iv
    except ValueError:
        return None


def calculate_time_to_expiry(val_date, exp_date):
    """Calculate time to expiry in years."""
    if isinstance(val_date, str):
        val_date = datetime.strptime(val_date, "%Y-%m-%d")
    if isinstance(exp_date, str):
        exp_date = datetime.strptime(exp_date, "%Y-%m-%d")

    days = (exp_date - val_date).days
    return days / 365.0


def format_vol(iv):
    """Format IV as percentage or N/A."""
    if iv is None:
        return "N/A"
    return f"{iv * 100:.2f}%"


def main():
    print("=" * 60)
    print("  OPTIONS IMPLIED VOLATILITY CALCULATOR")
    print("=" * 60)
    print()

    # Get inputs
    ticker = input("Ticker: ").upper().strip()

    # Fetch real underlying price from Yahoo Finance
    print(f"Fetching {ticker} price...")
    current_price = None
    try:
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            current_price = data['chart']['result'][0]['meta'].get('regularMarketPrice')
    except Exception as e:
        print(f"Error fetching price: {e}")

    if current_price:
        print(f"Current {ticker} price: ${current_price:.2f}")
        S = current_price
    else:
        print("Could not fetch price.")
        S = float(input("Underlying price: $"))

    exp_date = input("Expiration date (YYYY-MM-DD): ")
    K = float(input("Strike price: $"))
    option_type = input("Option type (call/put): ").lower().strip()
    val_date = input("Valuation date (YYYY-MM-DD): ")
    r = float(input("Risk-free rate (e.g., 0.05 for 5%): "))
    q = float(input("Dividend yield (e.g., 0.01 for 1%): "))

    # Get option prices (A required, B and C optional)
    price_a = float(input("Option price A: $"))

    price_b_input = input("Option price B (or Enter to skip): $").strip()
    price_b = float(price_b_input) if price_b_input else None

    price_c_input = input("Option price C (or Enter to skip): $").strip()
    price_c = float(price_c_input) if price_c_input else None

    # Calculate time to expiry
    T = calculate_time_to_expiry(val_date, exp_date)

    if T <= 0:
        print("\nError: Expiration date must be after valuation date.")
        return

    # Calculate implied volatilities
    vol_a = implied_volatility(price_a, S, K, T, r, q, option_type)
    vol_b = implied_volatility(price_b, S, K, T, r, q, option_type) if price_b else None
    vol_c = implied_volatility(price_c, S, K, T, r, q, option_type) if price_c else None

    # Build option description
    option_desc = f"{ticker} {exp_date} {K:.0f} {option_type.upper()}"

    # Print table
    print()
    print("=" * 100)
    print("  RESULTS")
    print("=" * 100)

    # Build header and row based on which prices were provided
    headers = ["Option", "Val Date", "Underlying", "r", "Div", "Price A", "Vol A"]
    values = [option_desc, val_date, f"${S:.2f}", f"{r*100:.2f}%", f"{q*100:.2f}%", f"${price_a:.2f}", format_vol(vol_a)]

    if price_b is not None:
        headers.extend(["Price B", "Vol B"])
        values.extend([f"${price_b:.2f}", format_vol(vol_b)])

    if price_c is not None:
        headers.extend(["Price C", "Vol C"])
        values.extend([f"${price_c:.2f}", format_vol(vol_c)])

    # Calculate column widths
    widths = [max(len(h), len(v)) + 2 for h, v in zip(headers, values)]

    # Print header
    header_row = "|".join(h.center(w) for h, w in zip(headers, widths))
    separator = "+".join("-" * w for w in widths)

    print(separator)
    print(header_row)
    print(separator)

    # Print values
    value_row = "|".join(v.center(w) for v, w in zip(values, widths))
    print(value_row)
    print(separator)



def parse_date(date_str):
    """Parse date in M/D/YYYY or YYYY-MM-DD format, return YYYY-MM-DD."""
    for fmt in ("%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    raise ValueError(f"Invalid date format: {date_str}. Use M/D/YYYY or YYYY-MM-DD.")


def fetch_price(ticker):
    """Fetch current price from Yahoo Finance."""
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=1d"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=10) as response:
        data = json.loads(response.read().decode())
        return data['chart']['result'][0]['meta'].get('regularMarketPrice')


def cli_mode(args):
    """Run IV calculation from command-line arguments."""
    if len(args) < 6:
        print("Usage: python options_vol_calculator.py TICKER EXP_DATE STRIKE call/put VAL_DATE PRICE_A [PRICE_B] [PRICE_C]")
        print("Example: python options_vol_calculator.py AAPL 3/31/2026 300 call 1/31/2026 10 20")
        return

    ticker = args[0].upper()
    exp_date = parse_date(args[1])
    K = float(args[2])
    option_type = args[3].lower()
    val_date = parse_date(args[4])
    prices = [float(p) for p in args[5:8]]  # up to 3 prices

    S = fetch_price(ticker)
    if S is None:
        print(f"Error: Could not fetch price for {ticker}")
        return

    r = 0.045
    # Estimate dividend yield
    q = 0.005 if ticker in ('AAPL', 'MSFT', 'JPM', 'JNJ', 'PG', 'KO', 'PEP', 'VZ', 'T', 'XOM', 'CVX') else 0.0

    T = calculate_time_to_expiry(val_date, exp_date)
    if T <= 0:
        print("Error: Expiration date must be after valuation date.")
        return

    option_desc = f"{ticker} {exp_date} {K:.0f} {option_type.upper()}"
    vols = [implied_volatility(p, S, K, T, r, q, option_type) for p in prices]

    # Build table
    headers = ["Option", "Val Date", "Underlying", "r", "Div"]
    values = [option_desc, val_date, f"${S:.2f}", f"{r*100:.2f}%", f"{q*100:.2f}%"]
    labels = ["A", "B", "C"]
    for i, (p, v) in enumerate(zip(prices, vols)):
        headers.extend([f"Price {labels[i]}", f"Vol {labels[i]}"])
        values.extend([f"${p:.2f}", format_vol(v)])

    widths = [max(len(h), len(v)) + 2 for h, v in zip(headers, values)]
    separator = "+".join("-" * w for w in widths)
    header_row = "|".join(h.center(w) for h, w in zip(headers, widths))
    value_row = "|".join(v.center(w) for v, w in zip(values, widths))

    print(separator)
    print(header_row)
    print(separator)
    print(value_row)
    print(separator)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        cli_mode(sys.argv[1:])
    else:
        main()
