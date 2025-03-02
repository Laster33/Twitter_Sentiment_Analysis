import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt
import seaborn as sns

# Download VADER lexicon if not already downloaded
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_tweet_sentiment(csv_file, text_column='text'):
    """
    Perform sentiment analysis on tweets from a CSV file.
    
    Parameters:
    -----------
    csv_file : str
        Path to the CSV file containing tweets
    text_column : str
        Name of the column containing the tweet text (default is 'text')
    
    Returns:
    --------
    DataFrame with original data and sentiment scores added
    """
    # Load the data
    print(f"Loading data from {csv_file}...")
    try:
        df = pd.read_csv(csv_file)
        print(f"Successfully loaded {len(df)} tweets.")
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return None
    
    # Check if text column exists
    if text_column not in df.columns:
        print(f"Error: Column '{text_column}' not found in the CSV file.")
        print(f"Available columns: {', '.join(df.columns)}")
        return None
    
    # Initialize the VADER sentiment analyzer
    print("Initializing sentiment analyzer...")
    sid = SentimentIntensityAnalyzer()
    
    # Perform sentiment analysis on each tweet
    print("Analyzing sentiment...")
    
    # Create empty columns for sentiment scores
    df['compound'] = 0.0
    df['positive'] = 0.0
    df['neutral'] = 0.0
    df['negative'] = 0.0
    df['sentiment'] = ''
    
    # Analyze each tweet
    for idx, row in df.iterrows():
        if idx % 1000 == 0 and idx > 0:
            print(f"Processed {idx} tweets...")
            
        try:
            tweet = str(row[text_column])
            sentiment_scores = sid.polarity_scores(tweet)
            
            # Store sentiment scores
            df.at[idx, 'compound'] = sentiment_scores['compound']
            df.at[idx, 'positive'] = sentiment_scores['pos']
            df.at[idx, 'neutral'] = sentiment_scores['neu']
            df.at[idx, 'negative'] = sentiment_scores['neg']
            
            # Classify sentiment based on compound score
            if sentiment_scores['compound'] >= 0.05:
                df.at[idx, 'sentiment'] = 'positive'
            elif sentiment_scores['compound'] <= -0.05:
                df.at[idx, 'sentiment'] = 'negative'
            else:
                df.at[idx, 'sentiment'] = 'neutral'
                
        except Exception as e:
            print(f"Error processing tweet at index {idx}: {e}")
    
    print("Sentiment analysis complete!")
    
    # Generate summary statistics
    sentiment_counts = df['sentiment'].value_counts()
    print("\nSentiment Distribution:")
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        print(f"{sentiment}: {count} tweets ({percentage:.2f}%)")
    
    # Save results to a new CSV file
    output_file = csv_file.replace('.csv', '_with_sentiment.csv')
    df.to_csv(output_file, index=False)
    print(f"\nResults saved to {output_file}")
    
    return df

def visualize_sentiment(df):
    """
    Create visualizations of the sentiment analysis results.
    
    Parameters:
    -----------
    df : DataFrame
        DataFrame containing the analyzed tweets with sentiment scores
    """
    # Set the style for the plots
    sns.set(style="whitegrid")
    
    # Create a figure with multiple subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Sentiment Distribution (Pie Chart)
    sentiment_counts = df['sentiment'].value_counts()
    axes[0, 0].pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%', 
                 colors=['green', 'gray', 'red'])
    axes[0, 0].set_title('Overall Sentiment Distribution')
    
    # Plot 2: Sentiment Distribution (Bar Chart)
    sns.countplot(x='sentiment', data=df, ax=axes[0, 1], 
                 order=['positive', 'neutral', 'negative'],
                 palette={'positive': 'green', 'neutral': 'gray', 'negative': 'red'})
    axes[0, 1].set_title('Sentiment Counts')
    axes[0, 1].set_xlabel('Sentiment')
    axes[0, 1].set_ylabel('Number of Tweets')
    
    # Plot 3: Compound Score Distribution
    sns.histplot(df['compound'], bins=50, ax=axes[1, 0], kde=True)
    axes[1, 0].set_title('Distribution of Compound Sentiment Scores')
    axes[1, 0].set_xlabel('Compound Score')
    axes[1, 0].set_ylabel('Frequency')
    
    # Plot 4: Positive, Neutral, and Negative Scores
    df_scores = df[['positive', 'neutral', 'negative']].mean().reset_index()
    df_scores.columns = ['Sentiment Component', 'Average Score']
    sns.barplot(x='Sentiment Component', y='Average Score', data=df_scores, ax=axes[1, 1])
    axes[1, 1].set_title('Average Sentiment Component Scores')
    axes[1, 1].set_ylim(0, 1)
    
    # Adjust layout and save the figure
    plt.tight_layout()
    plt.savefig('sentiment_analysis_results.png')
    print("Visualizations saved to sentiment_analysis_results.png")
    plt.show()

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python tweet_sentiment.py <csv_file> [text_column_name]")
        print("Default text column name is 'text' if not specified")
        sys.exit(1)
    
    csv_file = sys.argv[1]
    text_column = sys.argv[2] if len(sys.argv) > 2 else 'text'
    
    df = analyze_tweet_sentiment(csv_file, text_column)
    
    if df is not None:
        visualize_sentiment(df)
