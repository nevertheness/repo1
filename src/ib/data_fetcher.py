"""
IBKR Data Fetcher
Pulls option chain and underlying price data from Interactive Brokers.
Requires TWS or IB Gateway running locally. No trading functionality.

Usage:
    python scripts/ib/data_fetcher.py [TICKER] [--port PORT] [--paper]

Examples:
    python scripts/ib/data_fetcher.py AAPL
    python scripts/ib/data_fetcher.py AAPL --paper
    python scripts/ib/data_fetcher.py AAPL --port 7496
"""

import sys
import argparse
from ib_insync import IB, Stock, Option, util

# TWS ports: 7497 = paper trading, 7496 = live
# IB Gateway ports: 4002 = paper trading, 4001 = live
DEFAULT_PORT_LIVE  = 7496
DEFAULT_PORT_PAPER = 7497


def connect(port: int) -> IB:
    ib = IB()
    print(f"Connecting to TWS/IB Gateway on port {port}...")
    ib.connect("127.0.0.1", port, clientId=10, readonly=True)
    print(f"Connected: {ib.isConnected()}")
    return ib


def fetch_underlying_price(ib: IB, ticker: str) -> float | None:
    print(f"\n{'='*60}")
    print(f"  UNDERLYING PRICE: {ticker}")
    print(f"{'='*60}")

    contract = Stock(ticker, "SMART", "USD")
    ib.qualifyContracts(contract)
    [market_data] = ib.reqTickers(contract)
    price = market_data.marketPrice()

    if price and price == price:  # filters out nan
        print(f"  {ticker}: ${price:.2f}")
        return price
    else:
        last = market_data.last
        close = market_data.close
        price = last if last and last == last else close
        if price and price == price:
            label = "Last" if last and last == last else "Prior Close"
            print(f"  {ticker}: ${price:.2f} ({label})")
            return price
        print(f"  {ticker}: price unavailable (market may be closed)")
        return None


def fetch_option_chain(ib: IB, ticker: str) -> tuple[list[str], list[float]]:
    print(f"\n{'='*60}")
    print(f"  OPTION CHAIN: {ticker}")
    print(f"{'='*60}")

    underlying = Stock(ticker, "SMART", "USD")
    ib.qualifyContracts(underlying)

    chains = ib.reqSecDefOptParams(ticker, "", "STK", underlying.conId)
    if not chains:
        print("  No option chain data returned.")
        return [], []

    # Use the SMART exchange chain
    smart_chain = next((c for c in chains if c.exchange == "SMART"), chains[0])
    expirations = sorted(smart_chain.expirations)
    strikes = sorted(smart_chain.strikes)

    print(f"  Expirations available: {len(expirations)}")
    for i, exp in enumerate(expirations[:12]):  # show first 12
        print(f"    [{i:2d}] {exp}")
    if len(expirations) > 12:
        print(f"    ... and {len(expirations) - 12} more")

    print(f"\n  Strikes available: {len(strikes)}")
    return expirations, strikes


def fetch_option_quotes(
    ib: IB,
    ticker: str,
    expiration: str,
    strikes: list[float],
    underlying_price: float | None,
    num_strikes: int = 10,
) -> None:
    print(f"\n{'='*60}")
    print(f"  OPTION QUOTES: {ticker} exp {expiration}")
    print(f"{'='*60}")

    # Filter strikes near the money if we have underlying price
    if underlying_price:
        strikes_near_atm = sorted(
            strikes, key=lambda s: abs(s - underlying_price)
        )[:num_strikes]
        selected_strikes = sorted(strikes_near_atm)
        print(f"  Showing {num_strikes} strikes nearest ATM (${underlying_price:.2f})\n")
    else:
        selected_strikes = strikes[:num_strikes]
        print(f"  Showing first {num_strikes} strikes\n")

    # Build contracts for calls and puts
    contracts = []
    for strike in selected_strikes:
        for right in ("C", "P"):
            contracts.append(Option(ticker, expiration, strike, right, "SMART"))

    ib.qualifyContracts(*contracts)
    tickers = ib.reqTickers(*contracts)

    # Organize by strike
    quotes: dict[float, dict] = {}
    for ticker_data in tickers:
        c = ticker_data.contract
        strike = c.strike
        right = "call" if c.right == "C" else "put"
        quotes.setdefault(strike, {})[right] = {
            "bid": ticker_data.bid,
            "ask": ticker_data.ask,
        }

    # Print table
    header = f"  {'Strike':>8} | {'Call Bid':>9} {'Call Ask':>9} | {'Put Bid':>8} {'Put Ask':>8}"
    print(header)
    print(f"  {'-'*8}-+-{'-'*9}-{'-'*9}-+-{'-'*8}-{'-'*8}")

    atm_strike = min(selected_strikes, key=lambda s: abs(s - underlying_price)) if underlying_price else None

    for strike in selected_strikes:
        q = quotes.get(strike, {})
        call = q.get("call", {})
        put  = q.get("put",  {})

        def fmt(val):
            return f"${val:>7.2f}" if val and val == val and val > 0 else "       -"

        atm_marker = " <-- ATM" if strike == atm_strike else ""
        print(
            f"  {strike:>8.2f} | {fmt(call.get('bid'))} {fmt(call.get('ask'))} "
            f"| {fmt(put.get('bid'))} {fmt(put.get('ask'))}{atm_marker}"
        )


def interactive_mode(ib: IB) -> None:
    ticker = input("\nTicker: ").upper().strip()
    if not ticker:
        return

    underlying_price = fetch_underlying_price(ib, ticker)
    expirations, strikes = fetch_option_chain(ib, ticker)

    if not expirations:
        return

    exp_input = input("\nExpiration index (or press Enter to skip quotes): ").strip()
    if not exp_input:
        return

    try:
        exp_index = int(exp_input)
        expiration = expirations[exp_index]
    except (ValueError, IndexError):
        print("Invalid selection.")
        return

    fetch_option_quotes(ib, ticker, expiration, strikes, underlying_price)


def cli_mode(ib: IB, ticker: str) -> None:
    underlying_price = fetch_underlying_price(ib, ticker)
    expirations, strikes = fetch_option_chain(ib, ticker)

    if expirations:
        # Default: show quotes for the nearest expiration
        fetch_option_quotes(ib, ticker, expirations[0], strikes, underlying_price)


def main() -> None:
    parser = argparse.ArgumentParser(description="IBKR data fetcher (read-only)")
    parser.add_argument("ticker", nargs="?", help="Ticker symbol (e.g. AAPL)")
    parser.add_argument("--port", type=int, help="TWS/Gateway port")
    parser.add_argument("--paper", action="store_true", help="Use paper trading port (7497)")
    args = parser.parse_args()

    if args.port:
        port = args.port
    elif args.paper:
        port = DEFAULT_PORT_PAPER
    else:
        port = DEFAULT_PORT_LIVE

    print("=" * 60)
    print("  IBKR DATA FETCHER  (read-only, no trading)")
    print("=" * 60)

    try:
        ib = connect(port)
    except Exception as e:
        print(f"\nConnection failed: {e}")
        print("Make sure TWS or IB Gateway is running and API access is enabled.")
        sys.exit(1)

    try:
        if args.ticker:
            cli_mode(ib, args.ticker.upper())
        else:
            interactive_mode(ib)
    finally:
        ib.disconnect()
        print("\nDisconnected.")


if __name__ == "__main__":
    util.logToConsole(None)  # suppress ib_insync internal logs
    main()
