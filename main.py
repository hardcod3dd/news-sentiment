import feedparser
import openai

# Set up the OpenAI API client
openai.api_key = "api-key here"

# Function to analyze sentiment using ChatGPT
def analyze_sentiment(text):
    system_msg = "You are a helpful assistant."
    user_msg = f"Analyse the sentiment of the following text as single phrase either negative or positive : \"{text}\". The sentiment is: "
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                        messages=[{"role": "system", "content": system_msg},
                                         {"role": "user", "content": user_msg}])
    sentiment = response['choices'][0]['message']['content']
    return sentiment

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

        print(f"Title: {title}")
        print(f"Link: {link}")
        print(f"Sentiment: {sentiment}\n")

if __name__ == "__main__":
    # Define the RSS feed URL
    rss_feed_url = input("RSS Feed URL: ")

    # Analyze the sentiment of news headlines from the RSS feed
    analyze_rss_feed_sentiment(rss_feed_url)