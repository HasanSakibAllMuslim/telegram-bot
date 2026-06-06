import asyncio
import random
import os
from datetime import datetime, timezone
from telethon import TelegramClient, events
from groq import Groq

# এনভায়রনমেন্ট ভেরিয়েবল (হাগিং ফেস স্পেসে সেট করতে হবে)
API_ID = int(os.environ.get('API_ID'))
API_HASH = os.environ.get('API_HASH')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')

# সেশন স্ট্রিং ব্যবহার করব (ফাইল না রেখে)
SESSION_STRING = os.environ.get('SESSION_STRING', None)

client = Groq(api_key=GROQ_API_KEY)
processed_messages = set()

async def get_ai_reply(original_message):
    love_keywords = ['ভালোবাসি', 'love', 'প্রেম', '❤️', 'i love']
    if any(kw.lower() in original_message.lower() for kw in love_keywords):
        return "আমি এসব নিয়ে কথা বলতে চাই না, অন্য কিছু জানতে চান 😊"
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": original_message}],
            temperature=0.85,
            max_tokens=200
        )
        reply = completion.choices[0].message.content
        reply = reply.replace("তুই", "তুমি")
        return reply[:500]
    except Exception as e:
        return "দেখুন, একটু সমস্যা হচ্ছে 😅"

async def run_bot():
    """বট চালানোর মূল ফাংশন"""
    if SESSION_STRING:
        # সেশন স্ট্রিং ব্যবহার করলে ফাইলের দরকার নেই
        telegram = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)
    else:
        telegram = TelegramClient('bot_session', API_ID, API_HASH)
    
    @telegram.on(events.NewMessage(incoming=True))
    async def handle(event):
        me = await telegram.get_me()
        if event.sender_id == me.id or not event.raw_text:
            return
        
        reply = await get_ai_reply(event.raw_text)
        await asyncio.sleep(random.uniform(1, 2))
        await event.reply(reply)
        print(f"Replied to: {event.raw_text[:50]}")
    
    await telegram.start(phone=PHONE_NUMBER)
    print("Bot is running on Hugging Face Spaces!")
    await telegram.run_until_disconnected()
