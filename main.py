from app.scraper import scrape_all_news
from app.ai_processor import filter_important_news, rewrite_news
from app.database import save_news_to_db
import logging

logging.basicConfig(level=logging.INFO)

def run_pipeline():
    logging.info("খবর সংগ্রহ শুরু...")
    all_news = scrape_all_news()
    logging.info(f"মোট {len(all_news)}টি খবর পাওয়া গেছে")
    important_news = filter_important_news(all_news, max_news=5)
    logging.info(f"গুরুত্বপূর্ণ বাছাই করা হয়েছে {len(important_news)}টি")
    for news in important_news:
        rewritten = rewrite_news(news)
        save_news_to_db(news['title'], news['summary'], rewritten, news['source'], news['link'])
    logging.info("সব কাজ শেষ!")

if __name__ == "__main__":
    run_pipeline()
