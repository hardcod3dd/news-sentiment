import feedparser
import openai
import re 
import pandas as pd

# Set up the OpenAI API client
openai.api_key = "apikey"
final_result = []

# Function to analyze sentiment using ChatGPT
def analyze_sentiment(text):
    system_msg = "You are a helpful assistant."
    user_msg = f"Analyse the sentiment of the following text as single phrase either negative or positive : \"{text}\". The sentiment is: "
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=[{"role": "system", "content": system_msg},
                                         {"role": "user", "content": user_msg}])
    sentiment = response['choices'][0]['message']['content']
    return sentiment

def find_sentiment(text):
    # Define a regular expression pattern to match "positive," "negative," or "neutral" (case-insensitive)
    pattern = re.compile(r'(positive|negative|neutral)', re.IGNORECASE)

    # Search for the pattern in the text
    match = re.search(pattern, text)

    if match:
        # Extract the matched word and convert it to lowercase
        sentiment = match.group(0).lower()

        # Check the sentiment and return it
        if sentiment == "positive":
            return "positive"
        elif sentiment == "negative":
            return "negative"
        elif sentiment == "neutral":
            return "neutral"

    # If no sentiment word is found, return None
    return None

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
        final_result.append(find_sentiment(sentiment))

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