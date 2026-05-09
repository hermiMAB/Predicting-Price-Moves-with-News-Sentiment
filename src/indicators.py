import pandas as pd
import talib
import pynance as pn
import quantstats as qs
import logging

# Extend pandas with QuantStats methods for advanced reporting
qs.extend_pandas()

def apply_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculates SMA, EMA, RSI, MACD using TA-Lib, 
    alternative metrics using PyNance, and daily returns for QuantStats.
    """
    if df.empty or 'Close' not in df.columns:
        logging.error("Cannot compute indicators: DataFrame is empty or missing 'Close'.")
        return df
        
    # Create a copy to prevent modifying the original dataframe
    data = df.copy()
    
    # Ensure data is sorted chronologically before calculating indicators
    if 'Date' in data.columns:
        data = data.sort_values(by='Date')
        
    close_prices = data['Close']
    
    # --- 1. Moving Averages (TA-Lib) ---
    data['SMA_20'] = talib.SMA(close_prices, timeperiod=20)
    data['SMA_50'] = talib.SMA(close_prices, timeperiod=50)
    data['EMA_20'] = talib.EMA(close_prices, timeperiod=20)
    
    # --- 2. RSI & MACD (TA-Lib) ---
    data['RSI'] = talib.RSI(close_prices, timeperiod=14)
    macd, macdsignal, macdhist = talib.MACD(
        close_prices, fastperiod=12, slowperiod=26, signalperiod=9
    )
    data['MACD'] = macd
    data['MACD_Signal'] = macdsignal
    data['MACD_Hist'] = macdhist
    
    # --- 3. Alternative Metrics (PyNance) ---
    # Wrapped in a try-except block so it doesn't crash if PyNance throws a warning
    try:
        data['SMA_50_pn'] = pn.tech.sma(close_prices, window=50)
    except Exception as e:
        logging.warning(f"PyNance calculation skipped: {e}")

    # --- 4. Daily Returns (QuantStats & Task 3 Prep) ---
    # Formula: (Close_t - Close_{t-1}) / Close_{t-1}
    data['Daily_Return'] = close_prices.pct_change()
    
    logging.info("Technical indicators successfully applied.")
    return data

def print_quantstats_summary(df: pd.DataFrame):
    """
    Prints a professional snapshot of Sharpe Ratio and Max Drawdown.
    Ensures the index is datetime-compatible for QuantStats.
    """
    if 'Daily_Return' in df.columns:
        # Create a temporary series with Date as the index
        # QuantStats MUST have a DatetimeIndex to calculate Drawdown
        temp_df = df.set_index('Date')
        returns = temp_df['Daily_Return'].dropna()
        
        print(f"Sharpe Ratio: {qs.stats.sharpe(returns):.2f}")
        
        # Now this will work because returns.index[0] is a Timestamp, not an Int
        print(f"Max Drawdown: {qs.stats.max_drawdown(returns)*100:.2f}%")
    else:
        print("Error: 'Daily_Return' column not found.")