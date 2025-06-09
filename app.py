import streamlit as st
import feedparser
from datetime import datetime

# Set page layout
st.set_page_config(page_title="Battery Project News", layout="wide")

# Title and date
st.title("🔋 Battery & EV News – California Focus")
st.markdown(f"#### 📅 {datetime.now().strftime('%A, %B %d, %Y')}")
st.markdown("This dashboard shows the latest daily news related to battery recycling, EVs, and circular economy topics in California.")

# Define Google News RSS feeds
rss_feeds = {
    "🔁 California Battery Recycling": "https://news.google.com/rss/search?q=california+battery+recycling",
    "🗑️ EV Battery Disposal & End-of-Life": "https://news.google.com/rss/search?q=ev+battery+disposal+california",
    "🔄 Second-Life Applications": "https://news.google.com/rss/search?q=second+life+electric+vehicle+batteries",
    "📊 Material Flow Analysis of Lithium-Ion Batteries": "https://news.google.com/rss/search?q=material+flow+analysis+lithium+ion+batteries",
    "⚡ California EV Legislation & Recycling Policy": "https://news.google.com/rss/search?q=california+ev+battery+recycling+policy"
}

# Loop through topics and display top 5 news items each
for topic, url in rss_feeds.items():
    st.markdown(f"### {topic}")
    feed = feedparser.parse(url)

    if not feed.entries:
        st.markdown("_No articles found today._")
    else:
        for entry in feed.entries[:5]:
            st.markdown(f"- [{entry.title}]({entry.link})")

    st.markdown("---")
