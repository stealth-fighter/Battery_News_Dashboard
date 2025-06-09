import streamlit as st
import feedparser
from datetime import datetime, timedelta
import time

# --- Page setup ---
st.set_page_config(page_title="Battery Project News", layout="wide")

# --- Initialize session state ---
if "saved_articles" not in st.session_state:
    st.session_state.saved_articles = []

if "saved_research" not in st.session_state:
    st.session_state.saved_research = []

# --- Define RSS feeds ---
rss_feeds = {
    "🔁 California Battery Recycling": "https://news.google.com/rss/search?q=california+battery+recycling",
    "🗑️ EV Battery Disposal": "https://news.google.com/rss/search?q=ev+battery+disposal+california",
    "🔄 Second-Life Applications": "https://news.google.com/rss/search?q=second+life+electric+vehicle+batteries",
    "📊 Material Flow Analysis (Li-Ion Batteries)": "https://news.google.com/rss/search?q=material+flow+analysis+lithium+ion+batteries",
    "⚡ California EV Policy Updates": "https://news.google.com/rss/search?q=california+ev+battery+recycling+policy"
}

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["🔍 Live News", "📚 Research Papers", "💾 Saved Items"])

# --- Tab 1: Live News Feed ---
with tab1:
    st.title("🔋 Battery & EV News – California Focus")
    st.markdown(f"#### 📅 {datetime.now().strftime('%A, %B %d, %Y')}")
    st.markdown("Search and explore the latest articles on battery recycling, EVs, and California policy.")

    # Only search filter
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
                    if st.button("💾 Save", key=unique_key):
                        article_data = {"title": title, "link": link}
                        if article_data not in st.session_state.saved_articles:
                            st.session_state.saved_articles.append(article_data)
                results_found = True

        if not results_found:
            st.markdown("_No articles found matching your search._")

        st.markdown("---")

# --- Tab 2: Research Papers (Search + Save) ---
with tab2:
    st.title("📚 Research Papers – MDPI + ScienceDaily")

    search_term = st.text_input("🔍 Search research titles and abstracts:", "").lower()

    sources = {
        "🔋 MDPI – Batteries": "https://www.mdpi.com/rss/journal/batteries",
        "⚡ MDPI – Energies": "https://www.mdpi.com/rss/journal/energies",
        "🌍 MDPI – Sustainability": "https://www.mdpi.com/rss/journal/sustainability",
        "📰 ScienceDaily – Battery Tech": "https://www.sciencedaily.com/rss/matter_energy/batteries.xml"
    }

    for label, rss_url in sources.items():
        st.markdown(f"### {label}")
        feed = feedparser.parse(rss_url)

        if not feed.entries:
            st.markdown("_No papers found or RSS feed not available._")
        else:
            shown = 0
            for i, entry in enumerate(feed.entries[:10]):
                title = entry.get("title", "")
                link = entry.get("link", "#")
                summary = entry.get("summary", "")
                combined_text = f"{title.lower()} {summary.lower()}"

                if search_term and search_term not in combined_text:
                    continue

                col1, col2 = st.columns([0.85, 0.15])
                with col1:
                    st.markdown(f"**🔹 Title:** [{title}]({link})")
                    st.markdown(f"**🔍 Abstract:** {summary[:300]}...")
                with col2:
                    save_key = f"save_research_{i}_{label}"
                    if st.button("💾 Save", key=save_key):
                        paper_data = {"title": title, "link": link}
                        if paper_data not in st.session_state.saved_research:
                            st.session_state.saved_research.append(paper_data)

                st.markdown("---")
                shown += 1

            if shown == 0:
                st.markdown("_No matching research papers found._")

# --- Tab 3: Unified Saved Items (News + Research) ---
with tab3:
    st.title("💾 Saved Items")

    # --- Saved News Section ---
    st.subheader("🗞️ Saved News Articles")
    if not st.session_state.saved_articles:
        st.markdown("_You haven’t saved any news articles yet._")
    else:
        for i, article in enumerate(st.session_state.saved_articles):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"- [{article['title']}]({article['link']})")
            with col2:
                if st.button("🗑️ Unsave", key=f"unsave_news_{i}"):
                    st.session_state.saved_articles.pop(i)
                    st.experimental_rerun()

    st.markdown("---")

    # --- Saved Research Section ---
    st.subheader("📚 Saved Research Papers")
    if not st.session_state.saved_research:
        st.markdown("_You haven’t saved any research papers yet._")
    else:
        for i, paper in enumerate(st.session_state.saved_research):
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"- [{paper['title']}]({paper['link']})")
            with col2:
                if st.button("🗑️ Unsave", key=f"unsave_research_{i}"):
                    st.session_state.saved_research.pop(i)
                    st.experimental_rerun()
