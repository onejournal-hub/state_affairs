import google.generativeai as genai
import os
import logging

logging.basicConfig(level=logging.INFO)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.5-flash')

def filter_important_news(articles, max_news=5):
    if not articles:
        return []
    news_list = "\n".join([f"- {a['title']} ({a['source']})" for a in articles])
    prompt = f"নিচের খবরগুলোর মধ্যে সবচেয়ে গুরুত্বপূর্ণ {max_news}টি খবরের শিরোনাম কমা (,) দিয়ে আলাদা করে লেখ:\n{news_list}"
    try:
        response = model.generate_content(prompt)
        selected_titles = [t.strip() for t in response.text.split(',')]
        filtered = [a for a in articles if a['title'] in selected_titles]
        return filtered
    except Exception as e:
        logging.error(f"AI বাছাই করতে সমস্যা: {e}")
        return articles[:max_news]

def rewrite_news(article):
    prompt = f"খবরটি সম্পূর্ণ নতুন ও মৌলিক বাংলায় পুনর্লিখন কর (শুধু খবর লিখবে, কোনো মন্তব্য নয়):\nশিরোনাম: {article['title']}\nবিস্তারিত: {article['summary']}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logging.error(f"AI রিরাইট করতে সমস্যা: {e}")
        return article['summary']
