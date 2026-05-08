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