from supabase import create_client
import os
import logging

logging.basicConfig(level=logging.INFO)
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def save_news_to_db(title, original, rewritten, source, link):
    try:
        data = {
            'title': title,
            'original_content': original,
            'rewritten_content': rewritten,
            'source': source,
            'link': link
        }
        supabase.table('news').insert(data).execute()
        logging.info(f"খবর সংরক্ষিত: {title}")
    except Exception as e:
        logging.error(f"ডেটাবেসে সংরক্ষণ সমস্যা: {e}")
