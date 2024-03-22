import telebot
from telebot import types

# Bot tokenni bot fatherdan oling
bot = telebot.TeleBot("Telegram Bot token")

# foydalanuvchini kuzatuvchi dictionary
user_state = {}

# Start buyrug'i uchun command
@bot.message_handler(commands=['start'])
def start(message):
    # Rasmni va keyin habarni yuborish
    with open('Rasm path kampyuterda joylashgan adresi', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    # foydalanuvchiga boshlang'ich habar yuborish
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name if message.from_user.last_name else ''
    welcome_message = (
        f"Assalomu alaykum {first_name} {last_name}!\n\n"
        "Yo'llar tekis va ravon bo'lishiga o'z hissangizni qo'shing. Har bir ovozingiz uchun 15 000 so'mdan pul olasiz!\n"
        "Ovoz berish tugmasini bosing va ovoz bering, ovoz bergandan so'ng o'z telefon raqamingizni va skrinshot rasmni tashlab bering.\n"
        "Agar muammo bo'lsa yoki tushunmasangiz +998912345678ga tel qiling."
    )
    bot.send_message(message.chat.id, welcome_message)

    # Botda tugmalar yaratish
    keyboard = types.InlineKeyboardMarkup()
    voting_button = types.InlineKeyboardButton("🗳Ovoz berish", callback_data='voting')
    contact_button = types.InlineKeyboardButton("📞Kantakt", callback_data='contact')
    keyboard.row(voting_button, contact_button)

    # habar yuborish
    bot.send_message(message.chat.id, "Iltimos tanlang:", reply_markup=keyboard)


# ovoz berish tugmasini handl qilish
@bot.callback_query_handler(func=lambda call: call.data == 'voting')
def voting(call):
    # oldingi kelgan habarni o'chirish
    if call.message.chat.id in user_state:
        bot.delete_message(call.message.chat.id, user_state[call.message.chat.id])

    # bir nechta tanlash opsition beriladi
    voting_message = (
        "1. Telegram bot yoki Website orqali ovoz bering!\n"
        "2. Yakunlandi tugmasini bossib Skrinshot va telefon raqamingizni yozib qoldiring"
    )
    keyboard = types.InlineKeyboardMarkup()
    telegram_button = types.InlineKeyboardButton("🤖Telegram Bot", url='https://t.me/ochiqbudjet_3_bot?start=032315711009')
    website_button = types.InlineKeyboardButton("🌐Website", url='https://openbudget.uz/boards/initiatives/initiative/32/7b72bec7-2f5e-417a-9590-4bdb6ab98c11')
    done_button = types.InlineKeyboardButton("✅Yakunlandi", callback_data='done')
    keyboard.row(telegram_button, website_button)
    keyboard.row(done_button)
    msg = bot.send_message(call.message.chat.id, voting_message, reply_markup=keyboard)
    # Habar IDsini saqlab qolish
    user_state[call.message.chat.id] = msg.message_id


# Done tugmasini hand qilish
@bot.callback_query_handler(func=lambda call: call.data == 'done')
def done(call):
    # oldingi habarni o'chirish
    if call.message.chat.id in user_state:
        bot.delete_message(call.message.chat.id, user_state[call.message.chat.id])

    # rtelefon raqam so'rash
    bot.send_message(call.message.chat.id, "Iltimos, telefon raqamingizni kiriting:")
    # ma'lumotni saqalash
    user_state[call.message.chat.id] = 'phone'


# Kantak tugmasini saqlash
@bot.callback_query_handler(func=lambda call: call.data == 'contact')
def contact(call):
    # Oldingi habarni o'chirish
    if call.message.chat.id in user_state:
        bot.delete_message(call.message.chat.id, user_state[call.message.chat.id])

    # kantak tugmasi bosilganda beriladigan javob
    contact_message = (
        "Xatolik bo'lsa, ushbu raqamga qo'ng'iroq qiling:\n\n"
        "Bobomurodov Sanjarbek -> +998 97 039 80 08"
    )
    bot.send_message(call.message.chat.id, contact_message)


# tel raqam kiritlganda handle qilish
@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'phone')
def phone(message):
    if message.text.startswith("+998") and message.text[1:].isdigit():
        # tasdiqlovchi habar yuborish
        bot.forward_message(6124935422, message.chat.id, message.message_id)
        bot.send_message(message.chat.id, f"Kiritilgan telefon raqami: {message.text}")
        bot.send_message(message.chat.id, "Iltimos, skrinshot rasmni tashlang:")
        user_state[message.chat.id] = 'photo'
    else:
        # agar hato farmatda bo'lsa qayta so'rash
        bot.send_message(message.chat.id, "Telefon raqamingizni noto'g'ri formatda kiritdingiz. Iltimos, qaytadan kiriting.")


# rasmni handle qilish
@bot.message_handler(content_types=['photo'], func=lambda message: user_state.get(message.chat.id) == 'photo')
def photo(message):
    # rasmni saqlab qolish
    file_id = message.photo[-1].file_id
    
    # tasdiqlovchi habar
    bot.forward_message(6124935422, message.chat.id, message.message_id)
    bot.send_message(message.chat.id, "Rahmat! Skrinshot rasmni qabul qildik.")
    bot.send_message(message.chat.id, "Iltimos, karta raqamingizni tashlang:")
    user_state[message.chat.id] = 'card_number'


# carta raqamini handle qilish
@bot.message_handler(func=lambda message: user_state.get(message.chat.id) == 'card_number')
def card_number(message):
    # yig'ilgan ma'lumotni boshqaga jo'natish
    bot.forward_message(6124935422, message.chat.id, message.message_id)
    
    #ohirgi tasdiqlovchi habar
    bot.send_message(message.chat.id, "Rahmat! Biz telefon raqamingizni va karta raqamingizni qabul qildik. "
                                      "Tekshirib, pul o'tkazishidan so'ng xabar beramiz.")

# botni qayta qayta run qilib turish
bot.polling()