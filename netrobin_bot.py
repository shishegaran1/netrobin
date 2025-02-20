import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# توکن ربات شما
TOKEN = '7790329143:AAFeN8TPjkTwJF4oPicYvSnlq9RDCwNq_Ns'
bot = telebot.TeleBot(TOKEN)

# آیدی کانال شما
channel_id = '@netrobin'

# دیکشنری برای ذخیره تعداد لایک و دیسلایک‌ها
reactions = {}

# مدیریت ارسال عکس، ویدیو، PDF و MP3
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio'])
def handle_media(message):
    # دریافت کپشن (اگر وجود داشته باشد)
    caption = message.caption if message.caption else ''
    
    # ساخت منوی لایک و دیسلایک
    markup = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton('👍 0', callback_data='like')
    dislike_button = InlineKeyboardButton('👎 0', callback_data='dislike')
    markup.add(like_button, dislike_button)

    # اگر کاربر عکس ارسال کرده باشد
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        bot.send_photo(channel_id, file_id, caption=caption, reply_markup=markup)

    # اگر کاربر ویدیو ارسال کرده باشد
    elif message.content_type == 'video':
        file_id = message.video.file_id
        bot.send_video(channel_id, file_id, caption=caption, reply_markup=markup)

    # اگر کاربر فایل PDF ارسال کرده باشد
    elif message.content_type == 'document':
        if message.document.mime_type == 'application/pdf':
            file_id = message.document.file_id
            bot.send_document(channel_id, file_id, caption=caption, reply_markup=markup)

    # اگر کاربر فایل MP3 ارسال کرده باشد
    elif message.content_type == 'audio':
        file_id = message.audio.file_id
        bot.send_audio(channel_id, file_id, caption=caption, reply_markup=markup)

# مدیریت ارسال متن
@bot.message_handler(content_types=['text'])
def handle_text(message):
    # ارسال متن به کانال بدون منوی لایک و دیسلایک
    bot.send_message(channel_id, message.text)

# مدیریت کلیک روی دکمه‌ها
@bot.callback_query_handler(func=lambda call: True)
def handle_reactions(call):
    message_id = call.message.message_id
    data = call.data
    
    # ثبت واکنش‌ها
    if message_id not in reactions:
        reactions[message_id] = {'like': 0, 'dislike': 0}
    
    if data == 'like':
        reactions[message_id]['like'] += 1
    elif data == 'dislike':
        reactions[message_id]['dislike'] += 1
    
    # به‌روز رسانی دکمه‌ها
    markup = InlineKeyboardMarkup()
    like_button = InlineKeyboardButton(f"👍 {reactions[message_id]['like']}", callback_data='like')
    dislike_button = InlineKeyboardButton(f"👎 {reactions[message_id]['dislike']}", callback_data='dislike')
    markup.add(like_button, dislike_button)
    
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=message_id, reply_markup=markup)

# اجرای ربات
bot.polling()
