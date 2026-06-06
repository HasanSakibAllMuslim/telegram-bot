import asyncio
import random
import os
from datetime import datetime, timezone
from telethon import TelegramClient, events
from groq import Groq

# ============================================
# 📋 Environment Variables থেকে নেওয়া
# ============================================
API_ID = int(os.environ.get('API_ID', 33678168))
API_HASH = os.environ.get('API_HASH', '3e2a43d930ac6ff982ef50d4f6857751')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '+8801752932489')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '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')

# Session ফাইলের পাথ (Koyeb-এ persistent নয়, কিন্তু কাজ করবে)
SESSION_NAME = "telegram_bot_session"

# ============================================
# 🤖 ক্লায়েন্ট সেটআপ
# ============================================
client = Groq(api_key=GROQ_API_KEY)
telegram = TelegramClient(SESSION_NAME, API_ID, API_HASH)

# আপনার বাকি কোড (get_ai_reply, handle_messages, main ফাংশন)
# ... সেটা আগের মতই থাকবে ...

async def main():
    print("🚀 বট শুরু হচ্ছে...")
    await telegram.start(phone=PHONE_NUMBER)
    me = await telegram.get_me()
    print(f"✅ লগইন সফল: {me.first_name}")
    print("🎯 বট লাইভ! (Koyeb Cloud)")
    await telegram.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
