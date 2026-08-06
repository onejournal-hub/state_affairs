import feedparser
import logging
import requests

logging.basicConfig(level=logging.INFO)

def fetch_from_rss(feed_url, source_name, limit=5):
    articles = []
    try:
        # গুগল নিউজ যেন ব্লক না করে সেজন্য হেডার (User-Agent) সেট করা
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        response = requests.get(feed_url, headers=headers, timeout=15)
        
        # যদি URL কাজ না করে (৪০৪ বা অন্য কোনো এরর)
        if response.status_code != 200:
            logging.warning(f"{source_name} HTTP {response.status_code} - URL কাজ করছে না বা ব্লক করা হয়েছে।")
            return []
        
        # রেসপন্স থেকে ফিড পার্স করা
        feed = feedparser.parse(response.text)
        
        if not feed.entries:
            logging.warning(f"{source_name} থেকে কোনো এন্ট্রি পাওয়া যায়নি।")
            return []
        
        # প্রতিটি খবর থেকে টাইটেল, লিংক ও সামারি নেওয়া
        for entry in feed.entries[:limit]:
            # গুগল নিউজের সামারি কখনও কখনও খালি থাকে, তাই ডেসক্রিপশন ব্যবহার করা হচ্ছে
            summary = entry.get('summary', entry.get('description', 'বিস্তারিত দেখুন লিংকে'))
            
            articles.append({
                'title': entry.get('title', 'শিরোনাম নেই'),
                'link': entry.get('link', ''),
                'summary': summary,
                'source': source_name
            })
        logging.info(f"{source_name} থেকে {len(articles)}টি খবর নেওয়া হয়েছে")
        
    except Exception as e:
        logging.error(f"{source_name} থেকে খবর নিতে সমস্যা: {str(e)[:100]}")
    return articles

def scrape_all_news():
    all_news = []
    
    # গুগল নিউজের RSS ফিড (বাংলাদেশ ও রাজনীতি ভিত্তিক)
    rss_sources = [
        # ১. বাংলাদেশের শিরোনাম খবর (সব ক্যাটাগরি)
        ('https://news.google.com/rss?hl=bn&gl=BD&ceid=BD:bn', 'Google News (Bangladesh)'),
        
        # ২. শুধু রাজনীতি বিষয়ক খবর
        ('https://news.google.com/rss/search?q=%E0%A6%AC%E0%A6%BE%E0%A6%82%E0%A6%B2%E0%A6%BE%E0%A6%A6%E0%A7%87%E0%A6%B6+%E0%A6%B0%E0%A6%BE%E0%A6%9C%E0%A6%A8%E0%A7%80%E0%A6%A4%E0%A6%BF&hl=bn&gl=BD&ceid=BD:bn', 'Google News (Politics)'),
    ]
    
    for feed_url, name in rss_sources:
        all_news.extend(fetch_from_rss(feed_url, name))
    
    if not all_news:
        logging.warning("কোনো সোর্স থেকে খবর পাওয়া যায়নি! নেটওয়ার্ক চেক করুন।")
    
    return all_news
