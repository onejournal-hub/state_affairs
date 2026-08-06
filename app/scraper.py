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
    # একাধিক RSS ফিড (বাংলা নিউজ সাইট)
    rss_sources = [
        ('https://www.bdnews24.com/feed', 'bdnews24.com'),  # বিডিনিউজ২৪
        ('https://www.jugantor.com/rss', 'Jugantor'),       # যুগান্তর
        ('https://www.dailyinqilab.com/rss.xml', 'Inqilab'), # দৈনিক ইনকিলাব
        # ('http://feeds.prothomalo.com/prothomalo', 'Prothom Alo'), # প্রথম আলো (ঐচ্ছিক)
    ]
    for feed_url, name in rss_sources:
        all_news.extend(fetch_from_rss(feed_url, name))
    
    if not all_news:
        logging.warning("কোনো সোর্স থেকে খবর পাওয়া যায়নি! নেটওয়ার্ক বা ফিড চেক করুন।")
    
    return all_news
