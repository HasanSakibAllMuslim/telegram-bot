import asyncio
import random
import os
from datetime import datetime, timezone
from telethon import TelegramClient, events
from groq import Groq

# ============================================
# 📋 সব তথ্য এনভায়রনমেন্ট থেকে নিবে
# ============================================
API_ID = int(os.environ.get('API_ID', 33678168))
API_HASH = os.environ.get('API_HASH', '3e2a43d930ac6ff982ef50d4f6857751')
PHONE_NUMBER = os.environ.get('PHONE_NUMBER', '+8801752932489')
GROQ_API_KEY = os.environ.get('GROQ_API_KEY', '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')

# ============================================
# 🤖 ক্লায়েন্ট সেটআপ
# ============================================
client = Groq(api_key=GROQ_API_KEY)
telegram = TelegramClient('telegram_bot_session', API_ID, API_HASH)
processed_messages = set()

# ============================================
# 🧠 AI ফাংশন
# ============================================
async def get_ai_reply(original_message):
    love_keywords = ['ভালোবাসি', 'love', 'আই লাভ ইউ', 'পাগল', 'প্রেম', 'গার্লফ্রেন্ড', 
                     'বয়ফ্রেন্ড', 'ক্রাশ', 'হার্ট', 'i love', 'miss you', '❤️', 
                     '💕', '💖', 'চুমু', 'কিস', 'বিয়ে', 'রিলেশন', 'হৃদয়']
    
    love_detected = any(keyword.lower() in original_message.lower() for keyword in love_keywords)
    
    if love_detected:
        neutral_replies = [
            "আমি এসব নিয়ে কথা বলতে চাই না, অন্য কিছু জানতে চান 😊",
            "দুঃখিত, আমি শুধু সাধারণ কথাবার্তা বলতে পারি।",
            "এই বিষয়ে কথা বলা আমার জন্য সম্ভব না। অন্য কিছু বলবেন?"
        ]
        return random.choice(neutral_replies)
    
    prompt = f"""তুমি একজন বাস্তব টেলিগ্রাম ইউজার। তোমার নাম সাকিব। কেউ তোমাকে লিখেছে: "{original_message}"

নিয়ম:
1. উত্তর হবে ছোট ও স্বাভাবিক (২-৩ বাক্য)
2. "তুই" ব্যবহার করবে না, সবসময় "তুমি" বলবে
3. মনে হবে যেন আসল মানুষ টাইপ করছে

এখন উত্তর দাও:"""
    
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.85,
            max_tokens=200
        )
        reply = completion.choices[0].message.content
        reply = reply.replace("তুই", "তুমি").replace("তোকে", "তোমাকে").replace("তোর", "তোমার")
        return reply[:500]
    except Exception as e:
        print(f"❌ API Error: {e}")
        return "দেখুন, একটু প্রযুক্তিগত সমস্যা হচ্ছে 😅 আবার বলবেন?"

# ============================================
# 📨 মেসেজ হ্যান্ডলার
# ============================================
@telegram.on(events.NewMessage(incoming=True))
async def handle_messages(event):
    me = await telegram.get_me()
    if event.sender_id == me.id:
        return
    
    msg_id = f"{event.chat_id}_{event.message.id}"
    if msg_id in processed_messages:
        return
    processed_messages.add(msg_id)
    
    msg_date = event.message.date
    now = datetime.now(timezone.utc)
    if (now - msg_date).total_seconds() > 5:
        return
    
    message_text = event.raw_text
    if not message_text:
        return
    
    sender = await event.get_sender()
    sender_name = sender.first_name or "Unknown"
    
    print(f"\n📩 {datetime.now().strftime('%H:%M:%S')} - {sender_name}: {message_text[:60]}")
    
    reply = await get_ai_reply(message_text)
    print(f"🤖 রিপ্লাই: {reply[:60]}...")
    
    await asyncio.sleep(random.uniform(1, 2))
    await event.reply(reply)

# ============================================
# 🚀 বট স্টার্ট
# ============================================
async def main():
    print("🚀 বট শুরু হচ্ছে...")
    print(f"🔧 মডেল: llama-3.1-8b-instant")
    print(f"📊 রেট লিমিট: ৩০টি/মিনিট (১,৮০০টি/ঘন্টা)")
    
    await telegram.start(phone=PHONE_NUMBER)
    me = await telegram.get_me()
    print(f"✅ লগইন সফল: {me.first_name}")
    print("🎯 বট এখন লাইভ! (Railway Cloud)")
    print("🛑 বন্ধ করতে Ctrl+C\n")
    
    await telegram.run_until_disconnected()

# ============================================
# 👇 স্টার্ট পয়েন্ট
# ============================================
if __name__ == '__main__':
    print("══════════════════════════════════════════")
    print("     🧠 টেলিগ্রাম AI বট (Railway)")
    print("     🤖 মডেল: Llama 3.1 8B Instant")
    print("     📊 লিমিট: ১,৮০০ মেসেজ/ঘন্টা ✅")
    print("══════════════════════════════════════════\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 বট বন্ধ")
