import telebot
import requests
import time

# এখানে আপনার টেলিগ্রাম এবং প্যানেলের কি সরাসরি সেট করা আছে
BOT_TOKEN = "8631089383:AAHal0wuIjuY--tqpM-LD2EgvwnL6sllxs"
CRACKERJACK_API_KEY = "Fb1b32e3-a692-4632-a24b-17628dde2de7"
BASE_URL = "https://crackerjacksms.com/public/api"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = telebot.types.KeyboardButton("📱 Get Number")
        btn2 = telebot.types.KeyboardButton("❌ Delete Number")
        markup.row(btn1, btn2)
        bot.send_message(
            message.chat.id, 
            "👋 আমাদের নতুন ক্র্যাকারজ্যাক ওটিপি বটে আপনাকে স্বাগতম!\n\nনাম্বার নেওয়ার জন্য নিচে থাকা বোতামগুলো ব্যবহার করুন।", 
            reply_markup=markup
        )
    except Exception as e:
        print(f"Start Error: {e}")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    headers = {"mauthapi": CRACKERJACK_API_KEY}
    
    if message.text == "📱 Get Number":
        bot.send_message(message.chat.id, "🔄 ক্র্যাকারজ্যাক প্যানেল থেকে নতুন নাম্বার খোঁজা হচ্ছে, দয়া করে অপেক্ষা করুন...")
        data = {"rid": "26134"}
        
        try:
            # কোনো প্রক্সি নেই, সরাসরি রিকোয়েস্ট যাবে
            response = requests.post(f"{BASE_URL}/getnum", headers=headers, data=data, timeout=15).json()
            
            if response.get("code") == 200 and "data" in response:
                number = response["data"].get("number")
                bot.send_message(message.chat.id, f"✅ আপনার জন্য নতুন নাম্বার: `{number}`\n\n💬 ওটিপি (OTP) কোডের জন্য লাইভ অপেক্ষা করা হচ্ছে...", parse_mode="Markdown")
                
                for _ in range(30):
                    time.sleep(4)
                    otp_response = requests.get(f"{BASE_URL}/success-otp", headers=headers, timeout=15).json()
                    
                    if otp_response.get("code") == 200 and "data" in otp_response:
                        otp_text = otp_response["data"].get("message")
                        bot.send_message(message.chat.id, f"🎉 **নতুন ওটিপি কোড এসেছে!**\n\n💬 {otp_text}", parse_mode="Markdown")
                        return
                
                bot.send_message(message.chat.id, "❌ দুঃখিত, নির্ধারিত সময়ের মধ্যে কোনো ওটিপি কোড পাওয়া যায়নি।")
            else:
                bot.send_message(message.chat.id, "❌ এই মুহূর্তে প্যানেলে কোনো নাম্বার খালি নেই অথবা ব্যালেন্স শেষ।")
        except:
            bot.send_message(message.chat.id, "⚠️ ক্র্যাকারজ্যাক সার্ভারের সাথে সংযোগ করা যাচ্ছে না।")

    elif message.text == "❌ Delete Number":
        bot.send_message(message.chat.id, "⏳ আপনার নাম্বারটি বাতিল করার রিকোয়েস্ট পাঠানো হচ্ছে...")
        try:
            response = requests.post(f"{BASE_URL}/cancel-number", headers=headers, timeout=15).json()
            if response.get("code") == 200:
                bot.send_message(message.chat.id, "✅ নাম্বারটি সফলভাবে বাতিল করা হয়েছে।")
            else:
                bot.send_message(message.chat.id, "❌ বাতিল করার মতো কোনো একটিভ নাম্বার নেই।")
        except:
            bot.send_message(message.chat.id, "⚠️ রিকোয়েস্টটি সফল করা যায়নি।")

bot.infinity_polling(timeout=20, long_polling_timeout=10)
