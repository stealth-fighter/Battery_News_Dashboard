import streamlit as st
import feedparser
import requests
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
tab1, tab2, tab3 = st.tabs(["🔍 Live News", "💾 Saved Articles", "📚 Research Papers"])

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
                    unique_key = f"save_{i}_{topic}_{link}"
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

import feedparser  # already imported above

# --- Tab 3: Research Papers (Filtered MDPI + arXiv) ---
with tab3:
    st.title("📚 Research Papers – MDPI + arXiv (Filtered)")

    keywords = ["battery", "recycling", "lithium", "ev", "material flow"]

    sources = {
        "🔬 MDPI Batteries Journal": "https://www.mdpi.com/rss/journal/batteries",
        "📄 arXiv – Energy Systems": "https://export.arxiv.org/rss/eess.SY"
    }

    for source_name, rss_url in sources.items():
        st.markdown(f"### {source_name}")
        feed = feedparser.parse(rss_url)

        if not feed.entries:
            st.markdown("_No papers found or RSS feed not available._")
        else:
            shown = 0
            for entry in feed.entries:
                title = entry.get("title", "").lower()
                summary = entry.get("summary", "").lower()
                link = entry.get("link", "#")

                # Filter by keyword
                if any(keyword in title or keyword in summary for keyword in keywords):
                    st.markdown(f"**🔹 Title:** [{entry.title}]({link})")
                    st.markdown(f"**🔍 Abstract:** {entry.summary[:300]}...")
                    st.markdown("---")
                    shown += 1

                if shown >= 10:
                    break  # limit to 10 filtered results

            if shown == 0:
                st.markdown("_No relevant papers matched your keywords._")

