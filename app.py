import streamlit as st
import feedparser
from datetime import datetime

# --- Page setup ---
st.set_page_config(page_title="Battery Project News", layout="wide")

# --- Title and date ---
st.title("🔋 Battery & EV News – California Focus")
st.markdown(f"#### 📅 {datetime.now().strftime('%A, %B %d, %Y')}")
st.markdown("Stay updated with live news on battery recycling, EV policies, and circular economy topics.")

# --- Search input box ---
search_query = st.text_input("🔍 Search in article titles:", "")

# --- Define RSS feeds ---
rss_feeds = {
    "🔁 California Battery Recycling": "https://news.google.com/rss/search?q=california+battery+recycling",
    "🗑️ EV Battery Disposal": "https://news.google.com/rss/search?q=ev+battery+disposal+california",
    "🔄 Second-Life Applications": "https://news.google.com/rss/search?q=second+life+electric+vehicle+batteries",
    "📊 Material Flow Analysis (Li-Ion Batteries)": "https://news.google.com/rss/search?q=material+flow+analysis+lithium+ion+batteries",
    "⚡ California EV Policy Updates": "https://news.google.com/rss/search?q=california+ev+battery+recycling+policy"
}

# --- Display headlines with filtering ---
for topic, url in rss_feeds.items():
    st.markdown(f"### {topic}")
    feed = feedparser.parse(url)

    # Track if any articles match the search
    results_found = False

    for entry in feed.entries[:10]:  # Limit to top 10 results
        title = entry.title
        link = entry.link

        # Filter if search is active
        if search_query.strip() == "" or search_query.lower() in title.lower():
            st.markdown(f"- [{title}]({link})")
            results_found = True

    if not results_found:
        st.markdown("_No articles found matching your search._")

    st.markdown("---")
