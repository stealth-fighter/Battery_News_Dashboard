import streamlit as st
import feedparser
from datetime import datetime

# Page setup
st.set_page_config(page_title="Battery Project News", layout="wide")

st.title("🔋 Battery & EV News – California Focus")
st.markdown(f"#### 📅 {datetime.now().strftime('%A, %B %d, %Y')}")
st.markdown("Stay updated with live news on battery recycling, EV policies, and circular economy topics.")

# 🔍 Search bar
search_query = st.text_input("Search in article titles:", "")

# Google News RSS feeds
rss_feeds = {
    "🔁 California Battery Recycling": "https://news.google.com/rss/search?q=california+battery+recycling",
    "🗑️ EV Battery Disposal": "https://news.google.com/rss/search?q=ev+battery+disposal+california",
    "🔄 Second-Life Applications": "https://news.google.com/rss/search?q=second+life+electric+vehicle+batteries",
    "📊 Material Flow Analysis of Lithium-Ion Batteries": "https://news.google.com/rss/search?q=material+flow+analysis+lithium+ion+batteries",
    "⚡ California EV Policy": "https://news.google.com/rss/search?q=california+ev+battery+recycling+policy"
}

# Display news section-wise with optional search filter
for topic, url in rss_feeds.items():
    st.markdown(f"### {topic}")
    feed = feedparser.parse(url)

    found_any = False  # Track if any article matched
    for entry in feed.entries[:10]:
        title = entry.title
        link = entry.link

        if search_query.lower() in title.lower():
            st.markdown(f"- [{title}]({link})")
            found_any = True

    if not found_any:
        st.markdown("_No articles found matching your search._")

    st.markdown("---")
