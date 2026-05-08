import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def calculate_headline_lengths(df: pd.DataFrame, column_name: str = 'headline') -> pd.DataFrame:
    """
    Calculates the character length of each headline and adds it as a new column.
    
    Parameters:
    df (pd.DataFrame): The dataset containing the text.
    column_name (str): The name of the column to analyze.
    
    Returns:
    pd.DataFrame: The dataframe with a new 'headline_length' column.
    """
    logging.info(f"Calculating text lengths for column: '{column_name}'")
    
    # Drop any random missing values in the text column just to be safe
    df = df.dropna(subset=[column_name]).copy()
    
    # Calculate the length of each string
    df['headline_length'] = df[column_name].apply(str).apply(len)
    
    logging.info("Headline lengths calculated successfully.")
    return df




def get_unified_publishers(df: pd.DataFrame, column_name: str = 'publisher') -> pd.DataFrame:
    """
    Cleans the publisher column by converting email addresses to just the company name,
    and leaves regular publisher names as they are.
    """
    logging.info("Unifying publishers and extracting companies from emails...")
    
    def extract_company(text):
        if pd.isna(text):
            return "Unknown"
        
        text = str(text)
        if '@' in text:
            # Step 1: Get everything after the @ symbol
            domain = text.split('@')[-1]
            # Step 2: Get the company name before the first dot
            company = domain.split('.')[0]
            # Step 3: Capitalize it so it looks clean on the graph
            return company.capitalize()
        
        # If it's not an email, just return the original name
        return text
        
    df['unified_publisher'] = df[column_name].apply(extract_company)
    return df

def get_publication_trends(df: pd.DataFrame, date_column: str = 'date') -> pd.Series:
    """
    Analyzes the publication frequency over time by counting the number of articles published each day.
    """
    logging.info("Calculating daily publication trends...")
    
    # 1. Ensure the column is a proper datetime object (we use UTC to standardize)
    df['datetime'] = pd.to_datetime(df[date_column], errors='coerce', utc=True)
    
    # 2. Extract just the calendar date (YYYY-MM-DD) so we can group by day
    df['just_date'] = df['datetime'].dt.date
    
    # 3. Count the number of articles per day and sort them chronologically
    daily_counts = df.groupby('just_date').size()
    
    logging.info("Time-series aggregation complete.")
    return daily_counts