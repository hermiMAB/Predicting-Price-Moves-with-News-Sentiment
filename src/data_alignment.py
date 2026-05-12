import pandas as pd

import pandas as pd

def align_company_data(ticker, stock_data, sentiment_data):
    """
    Filters and aligns stock and sentiment data for a single specific company,
    and drops unnecessary columns to save memory.
    """
    
    # 1. Filter the sentiment dataset 
    company_news = sentiment_data[sentiment_data['stock'] == ticker].copy()
    
    # Check if we actually have data for this company to avoid errors
    if stock_data.empty or company_news.empty:
        print(f"Warning: Missing stock or news data for {ticker}")
        return pd.DataFrame() 
        
    # --- Standardize column names to capital 'Date' ---
    if 'date' in company_news.columns:
        company_news = company_news.rename(columns={'date': 'Date'})
    if 'date' in stock_data.columns:
        stock_data = stock_data.rename(columns={'date': 'Date'})
        
    # 2. Sort both by Date (required for merge_asof)
    stock_data = stock_data.sort_values('Date')
    company_news = company_news.sort_values('Date')
    
    # 3. Align the timing (snap news forward to the next trading day)
    aligned_company = pd.merge_asof(
        company_news, 
        stock_data, 
        on='Date', 
        direction='forward',
        suffixes=('_news', '_stock') 
    )
    
    # 4. CLEANING PHASE: Drop junk columns we don't need for the next steps
    junk_columns = ['Unnamed: 0', 'url', 'publisher', 'stock','returns']
    aligned_company = aligned_company.drop(columns=junk_columns, errors='ignore')
    
    return aligned_company
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Run this once to make sure VADER is downloaded
nltk.download('vader_lexicon', quiet=True)

def apply_vader_sentiment(df, text_column='headline'):
    """
    Analyzes text using VADER, adds scores, and cleans up the final dataset.
    """
    df_result = df.copy()
    sia = SentimentIntensityAnalyzer()
    
    compounds, labels = [], []
    
    for text in df_result[text_column]:
        if pd.isna(text):
            compounds.append(0.0)
            labels.append('neutral')
            continue
            
        scores = sia.polarity_scores(str(text))
        compound = scores['compound']
        
        if compound >= 0.05:
            label = "positive"
        elif compound <= -0.05:
            label = "negative"
        else:
            label = "neutral"
            
        compounds.append(compound)
        labels.append(label)
        
    # Attach only the most useful VADER columns
    df_result['vader_compound'] = compounds
    df_result['sentiment_label'] = labels
    
    # CLEANING PHASE: Drop any remaining noisy columns from the stock data 
    # (Optional: uncomment the line below if you don't need Open/High/Low/Adj Close)
    # df_result = df_result.drop(columns=['Open', 'High', 'Low', 'Adj Close'], errors='ignore')
    
    return df_result
import pandas as pd

def aggregate_daily_data(df):
    """
    Collapses multiple headlines into one daily average to resolve repetitions
    and prepares the data for correlation analysis.
    """
    # 1. Sort by Date to ensure everything is in order
    df = df.sort_values('Date')
    
    # 2. Group by Date to collapse repetitions (Weekends/Multiple headlines)
    # We take the MEAN of sentiment and the FIRST of the stock data
    daily_summary = df.groupby('Date').agg({
        'vader_compound': 'mean',   # The average daily sentiment signal
        'Daily_Return': 'first',    # The daily return already calculated
        'headline': 'count'         # Volume of news articles per day
    }).reset_index()
    
    # 3. Rename headline count for better readability
    daily_summary = daily_summary.rename(columns={'headline': 'article_count'})
    
    # 4. Drop the NaN row (usually the first row after a pct_change)
    daily_summary = daily_summary.dropna(subset=['Daily_Return'])
    
    return daily_summary



