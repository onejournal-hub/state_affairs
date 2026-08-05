from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client
import os

app = FastAPI(title="State Affairs API")

# ========== CORS সেটআপ (Vercel থেকে রিকোয়েস্ট অনুমতি) ==========
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # প্রোডাকশনে "*" ঠিক আছে, অথবা আপনার Vercel URL দিন
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    supabase = None
    print("Warning: Supabase credentials not set")

@app.get("/api/news")
def get_all_news(limit: int = 20):
    if supabase is None:
        return {"status": "error", "message": "Supabase not configured"}
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
