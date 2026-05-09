from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import logging

def get_top_keywords_and_phrases(df: pd.DataFrame, column_name: str = 'headline', n_gram: int = 1, top_n: int = 20) -> pd.DataFrame:
    """
    Extracts the most common keywords (1-gram) or phrases (2-gram, 3-gram) from text.
    
    Parameters:
    df: The dataframe.
    column_name: The column containing the text.
    n_gram: 1 for single words, 2 for two-word phrases (bigrams), etc.
    top_n: How many top results to return.
    """
    logging.info(f"Extracting top {top_n} phrases (n-gram={n_gram}) from '{column_name}'...")
    
    # Drop empty headlines
    text_data = df[column_name].dropna().astype(str)
    
    # CountVectorizer automatically removes punctuation, lowercases text, 
    # removes english stop words ('the', 'is'), and extracts n-grams!
    vectorizer = CountVectorizer(stop_words='english', ngram_range=(n_gram, n_gram))
    
    # Fit the vectorizer and count the words
    word_counts = vectorizer.fit_transform(text_data)
    
    # Sum up the counts for each word/phrase
    sum_words = word_counts.sum(axis=0)
    
    # Match the words to their counts
    words_freq = [(word, sum_words[0, idx]) for word, idx in vectorizer.vocabulary_.items()]
    
    # Sort them from highest to lowest
    words_freq = sorted(words_freq, key=lambda x: x[1], reverse=True)
    
    # Return as a clean DataFrame
    result_df = pd.DataFrame(words_freq[:top_n], columns=['Phrase', 'Frequency'])
    logging.info("Keyword extraction complete.")
    return result_df