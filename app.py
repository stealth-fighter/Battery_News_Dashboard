import streamlit as st
import feedparser
from datetime import datetime

st.set_page_config(page_title="Battery Project News", layout="wide")

st.title("🔋 Daily News – Battery Recycling & EVs in California")

# List of Google News RSS feeds
rss_feeds = {
    "California Battery Recycling": "https://news.google.com/rss/search?q=california+battery+recycling",
    "EV Battery Disposal": "https://news.google.com/rss/search?q=ev+battery+disposal+california",
    "Second-life Batteries": "https://news.google.com/rss/search?q=second+life+electric+vehicle+batteries",
    "Material Flow Analysis Lithium": "https://news.google.com/rss/search?q=material+flow+analysis+lithium+ion+battery"
}

# Show current date
st.subheader("🗓 " + datetime.now().strftime("%A, %B %d, %Y"))

# Loop through each RSS feed
for topic, url in rss_feeds.items():
    st.markdown(f"### 🔹 {topic}")
    feed = feedparser.parse(url)
    
    for entry in feed.entries[:5]:  # Show only top 5 articles
        st.markdown(f"- [{entry.title}]({entry.link})")
    st.markdown("---")
