import streamlit as st
import feedparser
from datetime import datetime

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

    search_query = st.text_input("🔍 Search in article titles:", "")

    for topic, url in rss_feeds.items():
        st.markdown(f"### {topic}")
        feed = feedparser.parse(url)
        results_found = False

        for i, entry in enumerate(feed.entries[:10]):
            title = entry.title
            link = entry.link

            if search_query.strip() == "" or search_query.lower() in title.lower():
                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    st.markdown(f"- [{title}]({link})")
                with col2:
                    # ✅ Use unique key using index to avoid DuplicateWidgetID
                    unique_key = f"save_{i}_{topic}"
                    if st.button("Save", key=unique_key):
                        article_data = {"title": title, "link": link}
                        if article_data not in st.session_state.saved_articles:
                            st.session_state.saved_articles.append(article_data)
                results_found = True

        if not results_found:
            st.markdown("_No articles found matching your search._")

        st.markdown("---")

# --- Tab 2: Saved Articles ---
with tab2:
    st.title("💾 Saved Articles")
    if not st.session_state.saved_articles:
        st.markdown("_You haven’t saved any articles yet._")
    else:
        for article in st.session_state.saved_articles:
            st.markdown(f"- [{article['title']}]({article['link']})")
