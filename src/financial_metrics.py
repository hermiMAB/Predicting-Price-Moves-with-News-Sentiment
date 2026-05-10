import pandas as pd
import pynance as pn

def add_financial_metrics(df):

    # Daily Returns
    df['Returns'] = df['Close'].pct_change()

    # Volatility
    df['Volatility_20'] = (
        df['Returns']
        .rolling(window=20)
        .std()
    )

    # Cumulative Returns
    df['Cumulative_Return'] = (
        1 + df['Returns']
    ).cumprod()

    return df