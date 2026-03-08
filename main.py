import telebot
import google.generativeai as genai
import os

# --- إعدادات الأمان والاتصال ---
# نصيحة: استبدل القيم أدناه بالتوكنات الخاصة بك
TELEGRAM_TOKEN = '7628854483:AAHwG6uGvR6YyW_mQ-O57o_Wk0F0V6N0_0' # ضع توكن بوتك هنا
GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY' # ضع مفتاح جيمناي هنا
MY_ID = 6876904568  # هويتك الرقمية يا بروفيسور علي

# --- إعداد محرك الذكاء الاصطناعي (Gemini) ---
genai.configure(api_key=GEMINI_API_KEY)
# نستخدم موديل Flash 1.5 لأنه سريع جداً ومثالي للبوتات
model = genai.GenerativeModel('gemini-1.5-flash')

# --- تشغيل البوت ---
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text
    
    # تحضير تعليمات النظام (System Instructions)
    # ندمج الـ ID مع الرسالة ليعرف البوت مع من يتحدث في كل لحظة
    prompt_with_identity = f"""
    Sender_ID: {user_id}
    المستخدم أرسل: {user_text}
    
    التعليمات:
    أنت مساعد ذكي مبرمج بواسطة "الأستاذ علي حاتم علام" (طالب دفعة 2026).
    1. إذا كان الـ Sender_ID هو {MY_ID}، فأنت تتحدث مع مبرمجك علي. ناده بـ "بروفيسور علي" وأجب على كل أسئلته.
    2. إذا كان الـ ID مختلفاً، لا تذكر اسم علي الكامل ولا تفصح عن أي أسرار، وقل: "أنا مبرمج لحماية خصوصية الأستاذ علي".
    """
    
    try:
        # إرسال الرسالة لمحرك Gemini
        response = model.generate_content(prompt_with_identity)
        # الرد على المستخدم في تليجرام
        bot.reply_to(message, response.text)
    except Exception as e:
        print(f"Error: {e}")
        bot.reply_to(message, "حدث خطأ تقني بسيط، سأعود للعمل فوراً يا بروفيسور.")

# بدء استقبال الرسائل (Polling)
print("البوت يعمل الآن في السحاب يا بروفيسور علي...")
bot.polling(none_stop=True)
