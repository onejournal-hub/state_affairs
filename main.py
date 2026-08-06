import sys
import logging
from app.scraper import scrape_all_news
from app.ai_processor import filter_important_news, rewrite_news
from app.database import save_news_to_db

logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def run_pipeline():
    try:
        logging.info("🚀 খবর সংগ্রহ শুরু হচ্ছে...")
        all_news = scrape_all_news()
        if not all_news:
            logging.warning("কোনো খবর পাওয়া যায়নি।")
            return
        
        logging.info(f"মোট {len(all_news)}টি খবর পাওয়া গেছে")
        
        important_news = filter_important_news(all_news, max_news=5)
        logging.info(f"গুরুত্বপূর্ণ বাছাই করা হয়েছে {len(important_news)}টি")
        
        for news in important_news:
            try:
                logging.info(f"✍️ রিরাইট করা হচ্ছে: {news['title']}")
                rewritten = rewrite_news(news)
                save_news_to_db(
                    title=news['title'],
                    original=news['summary'],
                    rewritten=rewritten,
                    source=news['source'],
                    link=news['link']
                )
            except Exception as e:
                logging.error(f"একটি খবর প্রসেস করতে সমস্যা: {e}")
                continue
        
        logging.info("✅ সব কাজ শেষ!")
    except Exception as e:
        logging.error(f"পাইপলাইনে গুরুতর ত্রুটি: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_pipeline()
