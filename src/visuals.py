import matplotlib.pyplot as plt
import pandas as pd

# =====================================================
# GLOBAL STYLE
# =====================================================

def set_visual_style():
    """Apply consistent chart styling."""

    plt.style.use('seaborn-v0_8-darkgrid')

    plt.rcParams['figure.figsize'] = (14, 7)
    plt.rcParams['figure.dpi'] = 120

    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.labelsize'] = 12

    plt.rcParams['legend.fontsize'] = 11


# =====================================================
# 1. PRICE + MOVING AVERAGES
# =====================================================

def plot_price_and_ma(df: pd.DataFrame, symbol: str):

    plot_data = df.tail(150)

    plt.figure(figsize=(14, 7))

    # Closing Price
    plt.plot(
        plot_data['Date'],
        plot_data['Close'],
        label='Closing Price',
        linewidth=2
    )

    # SMA 20
    if 'SMA_20' in plot_data.columns:
        plt.plot(
            plot_data['Date'],
            plot_data['SMA_20'],
            label='SMA 20',
            linestyle='--'
        )

    # SMA 50
    if 'SMA_50' in plot_data.columns:
        plt.plot(
            plot_data['Date'],
            plot_data['SMA_50'],
            label='SMA 50',
            linestyle=':'
        )

    # EMA 20
    if 'EMA_20' in plot_data.columns:
        plt.plot(
            plot_data['Date'],
            plot_data['EMA_20'],
            label='EMA 20',
            linestyle='-.'
        )

    plt.title(f'{symbol} Closing Price with Moving Averages')

    plt.xlabel('Date')
    plt.ylabel('Price')

    plt.legend()

    plt.tight_layout()
    plt.show()


# =====================================================
# 2. RSI PANEL
# =====================================================

def plot_rsi(df: pd.DataFrame, symbol: str):

    plot_data = df.tail(150)

    plt.figure(figsize=(14, 4))

    plt.plot(
        plot_data['Date'],
        plot_data['RSI'],
        label='RSI',
        linewidth=2
    )

    # Overbought
    plt.axhline(
        70,
        linestyle='--',
        alpha=0.7,
        label='Overbought (70)'
    )

    # Oversold
    plt.axhline(
        30,
        linestyle='--',
        alpha=0.7,
        label='Oversold (30)'
    )

    # Neutral
    plt.axhline(
        50,
        linestyle=':',
        alpha=0.5
    )

    plt.title(f'{symbol} Relative Strength Index (RSI)')

    plt.xlabel('Date')
    plt.ylabel('RSI')

    plt.ylim(0, 100)

    plt.legend()

    plt.tight_layout()
    plt.show()


# =====================================================
# 3. MACD PANEL
# =====================================================

def plot_macd(df: pd.DataFrame, symbol: str):

    plot_data = df.tail(150)

    plt.figure(figsize=(14, 5))

    # MACD Line
    plt.plot(
        plot_data['Date'],
        plot_data['MACD'],
        label='MACD',
        linewidth=2
    )

    # Signal Line
    plt.plot(
        plot_data['Date'],
        plot_data['MACD_Signal'],
        label='Signal Line',
        linestyle='--'
    )

    # Histogram
    plt.bar(
        plot_data['Date'],
        plot_data['MACD_Hist'],
        alpha=0.4,
        label='Histogram'
    )

    plt.axhline(0, linestyle=':')

    plt.title(f'{symbol} MACD Indicator')

    plt.xlabel('Date')
    plt.ylabel('MACD')

    plt.legend()

    plt.tight_layout()
    plt.show()


    