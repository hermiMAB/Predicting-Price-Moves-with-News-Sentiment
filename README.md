# Predicting Price Moves with News Sentiment

## Project Purpose
The goal of this project is to build a quantitative financial pipeline that extracts, processes, and analyzes historical financial news data and stock price action. Ultimately, this project utilizes Natural Language Processing (NLP) and statistical correlation to determine if daily news sentiment has a predictive relationship with stock market returns.

## Data Sources
1. **Financial News Dataset:** A comprehensive dataset of financial news headlines, publishers, and publication dates (loaded via CSV).
2. **Stock Market Data:** Historical daily stock prices (Open, High, Low, Close, Volume) for target companies including AAPL, AMZN, GOOG, META, and NVDA.

## Setup Instructions
To run this project locally, follow these steps:

1. **Clone the repository:**
   `git clone https://github.com/hermiMAB/Predicting-Price-Moves-with-News-Sentiment.git`
2. **Set up a virtual environment (Optional but recommended):**
   `python -m venv .venv`
   `source .venv/bin/activate` # On Windows use: .venv\Scripts\activate
3. **Install the dependencies:**
   `pip install -r requirements.txt`
4. **Run the Notebooks:**
   Navigate to the `notebooks/` folder and execute the Jupyter Notebooks sequentially.