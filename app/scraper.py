import feedparser
import logging

logging.basicConfig(level=logging.INFO)

def fetch_from_rss(feed_url, source_name, limit=5):
    articles = []
    try:
        feed = feedparser.parse(feed_url)
        if not feed.entries:
            logging.warning(f"{source_name} থেকে কোনো এন্ট্রি পাওয়া যায়নি")
        for entry in feed.entries[:limit]:
            articles.append({
                'title': entry.get('title', 'শিরোনাম নেই'),
                'link': entry.get('link', ''),
                'summary': entry.get('summary', ''),
                'source': source_name
            })
        logging.info(f"{source_name} থেকে {len(articles)}টি খবর নেওয়া হয়েছে")
    except Exception as e:
        logging.error(f"{source_name} থেকে খবর নিতে সমস্যা: {e}")
    return articles

def scrape_all_news():
    all_news = []
    # RSS ফিড সোর্স (আপনি চাইলে আরও যোগ করতে পারেন)
    rss_sources = [
        ('http://feeds.prothomalo.com/prothomalo', 'Prothom Alo'),
        # ('https://www.thedailystar.net/rss.xml', 'Daily Star'),  # যদি কাজ করে
    ]
    for feed_url, name in rss_sources:
        all_news.extend(fetch_from_rss(feed_url, name))
    return all_news
