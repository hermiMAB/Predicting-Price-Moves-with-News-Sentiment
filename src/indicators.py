import pandas as pd
import talib
import pynance as pn 
import quantstats as qs 
import logging 

def prepare_data(df):
    df = df.copy()

    # Enforce timezone consistency to prevent QuantStats errors later
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        df = df.sort_values('Date')
        
    # TA-Lib STRICTLY requires float64 types. This prevents silent crashes.
    if 'Close' in df.columns:
        df['Close'] = df['Close'].astype('float64')

    return df

def add_moving_averages(df):
    df['SMA_20'] = talib.SMA(df['Close'], timeperiod=20)
    df['SMA_50'] = talib.SMA(df['Close'], timeperiod=50)
    df['EMA_20'] = talib.EMA(df['Close'], timeperiod=20)
    return df

def add_rsi(df):
    df['RSI'] = talib.RSI(df['Close'], timeperiod=14)
    return df

def add_macd(df):
    macd, signal, hist = talib.MACD(
        df['Close'],
        fastperiod=12,
        slowperiod=26,
        signalperiod=9
    )
    df['MACD'] = macd
    df['MACD_Signal'] = signal
    df['MACD_Hist'] = hist
    return df

def add_financial_metrics(df):
    df['Daily_Return'] = df['Close'].pct_change()

    try:
        df['SMA_50_PyNance'] = pn.tech.sma(df['Close'], window=50)
    except Exception as e:
        # Replaced print with proper logging
        logging.warning(f"PyNance calculation skipped: {e}")

    return df

def print_performance_metrics(df):
    # Safe check: Only set the index if 'Date' is an actual column and not already the index!
    if 'Date' in df.columns:
        temp_df = df.set_index('Date')
    else:
        temp_df = df.copy()
        
    # Dropna is crucial here so QuantStats doesn't trip on the first row
    returns = temp_df['Daily_Return'].dropna()

    sharpe = qs.stats.sharpe(returns)
    drawdown = qs.stats.max_drawdown(returns)

    print(f"Sharpe Ratio: {sharpe:.2f}")
    print(f"Max Drawdown: {drawdown*100:.2f}%")