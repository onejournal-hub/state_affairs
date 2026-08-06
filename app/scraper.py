import feedparser
import logging
import requests
from bs4 import BeautifulSoup
import time

logging.basicConfig(level=logging.INFO)

def fetch_from_rss(feed_url, source_name, limit=5):
    articles = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(feed_url, headers=headers, timeout=15)
        if response.status_code != 200:
            logging.warning(f"{source_name} HTTP {response.status_code} - ব্লক বা ডাউন")
            return []
        feed = feedparser.parse(response.text)
        if not feed.entries:
            logging.warning(f"{source_name} - কোনো এন্ট্রি নেই")
            return []
        for entry in feed.entries[:limit]:
            summary = entry.get('summary', entry.get('description', ''))
            articles.append({
                'title': entry.get('title', 'শিরোনাম নেই'),
                'link': entry.get('link', ''),
                'summary': summary,
                'source': source_name
            })
        logging.info(f"{source_name} থেকে {len(articles)}টি খবর নেওয়া হয়েছে")
    except Exception as e:
        logging.error(f"{source_name} ERROR: {str(e)[:80]}")
    return articles

def scrape_from_website(url, source_name):
    """সরাসরি ওয়েবসাইট থেকে HTML স্ক্র্যাপিং (যদি RSS না চলে)"""
    articles = []
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            logging.warning(f"{source_name} স্ক্র্যাপ HTTP {response.status_code}")
            return []
        soup = BeautifulSoup(response.text, 'html.parser')
        # প্রথম আলোর জন্য (প্রথম আলো ডেস্কটপ ভার্সন)
        for item in soup.select('.story-card, .card, .article-card, .lead-story, h2 a')[:5]:
            title_tag = item
            if item.name == 'a':
                title = item.get_text(strip=True)
                link = item.get('href')
            else:
                title_tag = item.find('h2') or item.find('h3') or item.find('a')
                if not title_tag:
                    continue
                title = title_tag.get_text(strip=True)
                link = title_tag.get('href')
            if not title or len(title) < 5:
                continue
            if link and not link.startswith('http'):
                link = "https://www.prothomalo.com" + link
            articles.append({
                'title': title,
                'link': link,
                'summary': title,
                'source': source_name
            })
        logging.info(f"{source_name} থেকে {len(articles)}টি খবর স্ক্র্যাপ করা হয়েছে")
    except Exception as e:
        logging.error(f"{source_name} স্ক্র্যাপ ERROR: {str(e)[:80]}")
    return articles

def scrape_all_news():
    all_news = []
    
    # ১. আরএসএস ফিড যা এখনও কাজ করতে পারে (সর্বশেষ চেক করে)
    rss_sources = [
        ('https://www.prothomalo.com/feed', 'Prothom Alo RSS'),
        ('https://www.tbsnews.net/rss.xml', 'TBS News (Eng)'),  # ইংরেজি, কিন্তু কাজ করে
    ]
    for feed_url, name in rss_sources:
        all_news.extend(fetch_from_rss(feed_url, name))
        time.sleep(1)
    
    # ২. যদি RSS থেকে না আসে, সরাসরি স্ক্র্যাপিং (প্রথম আলো)
    if len(all_news) < 3:
        logging.info("RSS থেকে পর্যাপ্ত খবর না আসায় সরাসরি স্ক্র্যাপিং চালু...")
        all_news.extend(scrape_from_website('https://www.prothomalo.com/', 'Prothom Alo (Web)'))
    
    # ৩. এখনও কিছু না পেলে, ইউটিউব বা অন্য কিছু নয়, আমরা খালি রিটার্ন করব
    if not all_news:
        logging.warning("কোনো সোর্স থেকে খবর পাওয়া যায়নি! নেটওয়ার্ক বা ব্লকিং সমস্যা।")
    
    return all_news
