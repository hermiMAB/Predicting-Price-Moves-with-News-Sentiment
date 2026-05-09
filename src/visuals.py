import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def set_visual_style():
    """Sets the global chart style as per the tutorial reference."""
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = [12, 7]
    plt.rcParams['figure.dpi'] = 100

def plot_price_and_ma(df: pd.DataFrame, symbol: str):
    """
    Requirement 4a: Plot closing prices overlaid with moving averages.
    Uses the 150-day window and specific styles from the reference.
    """
    plot_data = df.tail(150)
    
    plt.figure(figsize=(12, 8))
    plt.plot(plot_data['Date'], plot_data['Close'], label='Close', color='black', linewidth=1.5)
    
    # Plot Multiple Moving Averages
    if 'SMA_20' in plot_data.columns:
        plt.plot(plot_data['Date'], plot_data['SMA_20'], label='SMA 20', linestyle='--')
    if 'SMA_50' in plot_data.columns:
        plt.plot(plot_data['Date'], plot_data['SMA_50'], label='SMA 50', linestyle=':')
    if 'EMA_20' in plot_data.columns:
        plt.plot(plot_data['Date'], plot_data['EMA_20'], label='EMA 20', linestyle='-.')
        
    plt.title(f"{symbol} Price Action & Moving Averages")
    plt.legend()
    plt.show()

def plot_momentum_panels(df: pd.DataFrame):
    """
    Requirement 4b & 4c: RSI and MACD in separate panels.
    Includes the MACD Histogram and RSI Overbought/Oversold thresholds.
    """
    plot_data = df.tail(150)
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, 
                                   gridspec_kw={'height_ratios': [1, 1]})

    # Panel 1: MACD (Momentum Shift)
    if 'MACD' in plot_data.columns:
        ax1.plot(plot_data['Date'], plot_data['MACD'], label='MACD')
        ax1.plot(plot_data['Date'], plot_data['MACD_Signal'], label='Signal')
        ax1.bar(plot_data['Date'], plot_data['MACD_Hist'], label='Hist', alpha=0.3)
        ax1.set_title("MACD (Momentum Shift)")
        ax1.legend(loc='upper left')

    # Panel 2: RSI (Overbought/Oversold)
    if 'RSI' in plot_data.columns:
        ax2.plot(plot_data['Date'], plot_data['RSI'], color='purple', label='RSI')
        ax2.axhline(70, color='red', linestyle='--', alpha=0.5)
        ax2.axhline(30, color='green', linestyle='--', alpha=0.5)
        ax2.set_title("RSI (Overbought/Oversold)")
        ax2.legend(loc='upper left')

    plt.tight_layout()
    plt.show()