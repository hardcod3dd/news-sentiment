import feedparser
import pandas as pd
from transformers import pipeline

final_result = []

# Function to analyze sentiment using ChatGPT
def analyze_sentiment(text):
    classifier = pipeline("zero-shot-classification", model="MoritzLaurer/mDeBERTa-v3-base-mnli-xnli")
    sequence_to_classify = text
    candidate_labels = ["positive", "negative", "neutral"]
    output = classifier(sequence_to_classify, candidate_labels, multi_label=False)
    return max(zip(output['scores'], output['labels']))[1]

# Function to fetch news headlines from an RSS feed and analyze sentiment
def analyze_rss_feed_sentiment(feed_url):
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    if 'entries' not in feed:
        print("No news entries found in the RSS feed.")
        return

    for entry in feed.entries:
        title = entry.get('title', '')
        link = entry.get('link', '')

        # Analyze the sentiment of the news headline
        sentiment = analyze_sentiment(title)
        final_result.append(sentiment)
    
if __name__ == "__main__":
    # Define the RSS feed URL
    rss_feed_url = input("RSS Feed URL: ")

    # Analyze the sentiment of news headlines from the RSS feed
    analyze_rss_feed_sentiment(rss_feed_url)

    # Count the occurrences of positive and negative values (excluding neutral)
    series = pd.Series(final_result)
    non_neutral_series = series[series != 'neutral']
    value_counts = non_neutral_series.value_counts()

    # Calculate the percentages
    total_values = len(series)
    positive_percentage = (value_counts.get('positive', 0) / total_values) * 0.4 * 100
    negative_percentage = (value_counts.get('negative', 0) / total_values) * 0.6 * 100

    # Calculate the percentage
    percentage = positive_percentage + negative_percentage

    if percentage <= 50:
        print('The final score is Negative')
    else:
        print('The final result is Positive')