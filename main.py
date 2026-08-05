from fastapi import FastAPI
from supabase import create_client
import os

# এনভায়রনমেন্ট ভেরিয়েবল রেন্ডার থেকে নেওয়া হবে (load_dotenv প্রয়োজন নেই)
app = FastAPI(title="State Affairs API")

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

@app.get("/api/news")
def get_all_news(limit: int = 20):
    try:
        response = supabase.table('news')\
            .select('*')\
            .order('published_at', desc=True)\
            .limit(limit)\
            .execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/")
def health_check():
    return {"status": "State Affairs API is running!"}
