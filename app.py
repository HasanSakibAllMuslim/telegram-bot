from fastapi import FastAPI
import asyncio
import threading
import os
from bot import run_bot

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Telegram Bot is running on Hugging Face Spaces!"}

# ব্যাকগ্রাউন্ডে বট চালানোর ফাংশন
def start_bot():
    asyncio.run(run_bot())

# স্পেস স্টার্ট হলে বট চালু হবে
threading.Thread(target=start_bot, daemon=True).start()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
