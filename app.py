import streamlit as st
import feedparser
from datetime import datetime, timedelta
import time

# --- Page setup ---
st.set_page_config(page_title="Battery Project News", layout="wide")

# --- Initialize session state for saved articles ---
if "saved_articles" not in st.session_state:
    st.session_state.saved_articles = []

# --- Define RSS feeds ---
rss_feeds = {
    "🔁 California Battery Recycling": "https://news.google.com/rss/search?q=california+battery+recycling",
    "🗑️ EV Battery Disposal": "https://news.google.com/rss/search?q=ev+battery+disposal+california",
    "🔄 Second-Life Applications": "https://news.google.com/rss/search?q=second+life+electric+vehicle+batteries",
    "📊 Material Flow Analysis (Li-Ion Batteries)": "https://news.google.com/rss/search?q=material+flow+analysis+lithium+ion+batteries",
    "⚡ California EV Policy Updates": "https://news.google.com/rss/search?q=california+ev+battery+recycling+policy"
}

# --- Tabs ---
tab1, tab2 = st.tabs(["🔍 Live News", "💾 Saved Articles"])

# --- Tab 1: Live News Feed ---
with tab1:
    st.title("🔋 Battery & EV News – California Focus")
    st.markdown(f"#### 📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    st.markdown("Search and explore the latest articles on battery recycling, EVs, and California policy.")

    # Search and filter options
    search_query = st.text_input("🔍 Search in article titles:", "")
    filter_range = st.radio("🕒 Show articles from:", ["Today", "This Week"], horizontal=True)

    now = datetime.utcnow()
    cutoff_today = now.date()
    cutoff_week = now - timedelta(days=7)

    for topic, url in rss_feeds.items():
        st.markdown(f"### {topic}")
        feed = feedparser.parse(url)
        results_found = False

        for i, entry in enumerate(feed.entries[:10]):
            title = entry.title
            link = entry.link
            published = getattr(entry, "published_parsed", None)

            # Parse publish date if available
            if published:
                published_dt = datetime.fromtimestamp(time.mktime(published))
                pub_date = published_dt.date()
            else:
                pub_date = None  # Allow missing dates

            # Apply keyword and date filter
            matches_keyword = (search_query.strip() == "" or search_query.lower() in title.lower())

            if filter_range == "Today":
                matches_date = (pub_date == cutoff_today if pub_date else True)
            elif filter_range == "This Week":
                matches_date = (pub_date >= cutoff_week.date() if pub_date else True)
            else:
                matches_date = True

            show_article = matches_keyword and matches_date

            if show_article:
                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    st.markdown(f"- [{title}]({link})")
                with col2:
                    unique_key = f"save_{i}_{topic}_{link}"
                    if st.button("Save", key=unique_key):
                        article_data = {"title": title, "link": link}
                        if article_data not in st.session_state.saved_articles:
                            st.session_state.saved_articles.append(article_data)
                results_found = True

        if not results_found:
            st.markdown("_No articles found matching your filters._")

        st.markdown("---")

# --- Tab 2: Saved Articles ---
with tab2:
    st.title("💾 Saved Articles")
    if not st.session_state.saved_articles:
        st.markdown("_You haven’t saved any articles yet._")
    else:
        for article in st.session_state.saved_articles:
            st.markdown(f"- [{article['title']}]({article['link']})")
