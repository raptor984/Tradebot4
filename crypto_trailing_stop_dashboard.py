
import ccxt
import pandas as pd
import numpy as np
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt

st.title("Crypto Trailing Stop Backtester")

percent_change = st.slider("Required Percent Change (per hour)", 0.01, 0.20, 0.05, 0.01)
trailing_stop_pct = st.slider("Trailing Stop Percent", 0.005, 0.05, 0.02, 0.005)
lookback_hours = st.slider("Lookback Hours", 24, 720, 720, 24)

exchange = ccxt.binanceus()
markets = exchange.load_markets()
symbols = [s for s in markets if s.endswith('/USDT')]

def trailing_stop(prices, entry, trailing_pct):
    peak = entry
    for price in prices:
        if price > peak:
            peak = price
        stop = peak * (1 - trailing_pct)
        if price < stop:
            return stop
    return prices[-1]

results = []

progress = st.progress(0)
total = len(symbols)

for idx, symbol in enumerate(symbols):
    st.write(f"Processing {symbol}...")
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=lookback_hours)
        df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        for i in range(1, len(df)):
            pct = (df['close'][i] - df['close'][i-1]) / df['close'][i-1]
            if pct >= percent_change:
                entry = df['close'][i]
                future = df['close'][i+1:].values
                if len(future) == 0:
                    continue
                exit = trailing_stop(future, entry, trailing_stop_pct)
                profit = (exit - entry) / entry
                results.append({
                    'symbol': symbol,
                    'entry_time': datetime.utcfromtimestamp(df['timestamp'][i]/1000),
                    'entry_price': entry,
                    'exit_price': exit,
                    'profit_pct': profit
                })
    except Exception as e:
        st.write(f"{symbol} failed: {e}")
    progress.progress((idx + 1) / total)

df_results = pd.DataFrame(results)
st.write(df_results)

st.write(f"Total Trades: {len(df_results)}")
st.write(f"Average Profit: {df_results['profit_pct'].mean():.4%}")
st.write(f"Total Cumulative Return: {(1 + df_results['profit_pct']).prod() - 1:.2%}")

if not df_results.empty:
    fig, ax = plt.subplots()
    ax.hist(df_results['profit_pct'] * 100, bins=30, edgecolor='k')
    ax.set_title("Profit per Trade (%)")
    ax.set_xlabel("Profit %")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    df_sorted = df_results.sort_values('entry_time')
    df_sorted['cum_return'] = (1 + df_sorted['profit_pct']).cumprod() - 1

    fig2, ax2 = plt.subplots()
    ax2.plot(df_sorted['entry_time'], df_sorted['cum_return'] * 100)
    ax2.set_title("Cumulative Return Over Time")
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Cumulative Return %")
    st.pyplot(fig2)

    df_results.to_csv("streamlit_backtest_results.csv", index=False)
    st.write("Results saved to streamlit_backtest_results.csv")
