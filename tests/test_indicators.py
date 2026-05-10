import pandas as pd
import numpy as np
from src.indicators import calculate_sma # Make sure this matches your actual import path!

def test_calculate_sma():
    """Tests if the SMA function correctly adds a new column."""
    #  stock data (30 days of random prices)
    data = {'Close': np.random.rand(30) * 100}
    df = pd.DataFrame(data)
    
    # 2. Run your function
    result_df = calculate_sma(df, sma_window=20)
    
    # 3. Assert that the new column was successfully created
    assert 'SMA_20' in result_df.columns