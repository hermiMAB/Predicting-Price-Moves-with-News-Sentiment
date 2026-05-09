import pandas as pd
import logging

# Set up logging to track the process
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_data(file_path: str) -> pd.DataFrame:
    """
    Loads the financial news CSV file into a Pandas DataFrame.
    
    Parameters:
    file_path (str): The relative or absolute path to the CSV file.
    
    Returns:
    pd.DataFrame: The loaded dataset, or None if the file is not found.
    """
    try:
        logging.info(f"Attempting to load data from: {file_path}")
        # We load it and immediately parse the dates to save time later
        df = pd.read_csv(file_path, parse_dates=['date'])
        logging.info(f"Success! Loaded {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    
    except FileNotFoundError:
        logging.error(f"Could not find the file at {file_path}. Please check your path.")
        return None


import pandas as pd
import os
import logging

def load_stock_data(file_path: str) -> pd.DataFrame:
    """
    Strictly responsible for loading the CSV, enforcing data types, 
    and removing completely corrupted/empty rows.
    """
    if not os.path.exists(file_path):
        logging.error(f"File not found: {file_path}")
        return pd.DataFrame()
        
    # Load the raw data
    df = pd.read_csv(file_path)
    
    # Enforce Date formatting
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], utc=True)
        
    # Enforce numeric formatting for all specific columns
    price_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    for col in price_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            
    if 'Volume' in df.columns:
        df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce')
        
    # Drop ONLY rows where every single column is missing (junk rows)
    df = df.dropna(how='all')
    
    return df


def process_financial_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strictly responsible for applying financial missing-value rules 
    (forward-fill prices, zero-fill volume) to prevent look-ahead bias.
    """
    if df.empty:
        return df
        
    clean_df = df.copy()
    
    # 1. Sort chronologically (CRITICAL before forward-filling)
    if 'Date' in clean_df.columns:
        clean_df = clean_df.sort_values(by='Date')
        
    # 2. Apply Forward-Fill to prices
    price_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close']
    for col in price_cols:
        if col in clean_df.columns:
            clean_df[col] = clean_df[col].ffill()
            
    # 3. Apply Zero-Fill to Volume
    if 'Volume' in clean_df.columns:
        clean_df['Volume'] = clean_df['Volume'].fillna(0)
        
    # 4. Standard DropNA for any lingering NaNs (e.g., the very first day)
    clean_df = clean_df.dropna()
    
    return clean_df