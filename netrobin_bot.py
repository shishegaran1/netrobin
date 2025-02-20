import os
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# 🔹 قبل از اجرای پروژه در ویندوز، این دستورات را در CMD اجرا کن:
# set TOKEN=توکن_ربات_اینجا
# set CHANNEL_ID=@netrobin

# دریافت مقادیر از متغیرهای محیطی
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# بررسی اینکه مقادیر به درستی دریافت شده‌اند
if not TOKEN or not CHANNEL_ID:
    raise ValueError("❌ خطا: مقادیر TOKEN و CHANNEL_ID تنظیم نشده‌اند!")

bot = telebot.TeleBot(TOKEN)

# دیکشنری برای ذخیره تعداد لایک و دیسلایک‌ها
reactions = {}

# مدیریت ارسال عکس، ویدیو، PDF و MP3
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio'])
def handle_media(message):
    caption = message.caption if message.caption else ''
    
    markup = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton('👍 0', callback_data='like')
    dislike_button = InlineKeyboardButton('👎 0', callback_data='dislike')
    markup.add(like_button, dislike_button)

    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        bot.send_photo(CHANNEL_ID, file_id, caption=caption, reply_markup=markup)

    elif message.content_type == 'video':
        file_id = message.video.file_id
        bot.send_video(CHANNEL_ID, file_id, caption=caption, reply_markup=markup)

    elif message.content_type == 'document' and message.document.mime_type == 'application/pdf':
        file_id = message.document.file_id
        bot.send_document(CHANNEL_ID, file_id, caption=caption, reply_markup=markup)

    elif message.content_type == 'audio':
        file_id = message.audio.file_id
        bot.send_audio(CHANNEL_ID, file_id, caption=caption, reply_markup=markup)

# مدیریت ارسال متن
@bot.message_handler(content_types=['text'])
def handle_text(message):
    bot.send_message(CHANNEL_ID, message.text)

# مدیریت کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def handle_reactions(call):
    message_id = call.message.message_id
    data = call.data
    
    if message_id not in reactions:
        reactions[message_id] = {'like': 0, 'dislike': 0}
    
    if data == 'like':
        reactions[message_id]['like'] += 1
    elif data == 'dislike':
        reactions[message_id]['dislike'] += 1
    
    markup = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton(f"👍 {reactions[message_id]['like']}", callback_data='like')
    dislike_button = InlineKeyboardButton(f"👎 {reactions[message_id]['dislike']}", callback_data='dislike')
    markup.add(like_button, dislike_button)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=message_id, reply_markup=markup)

# اجرای ربات
print("✅ ربات در حال اجرا است...")
bot.polling()
