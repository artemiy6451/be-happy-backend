from time import sleep

import telebot
from config import Settings
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

# Ваш токен
bot = telebot.TeleBot(Settings().token)


@bot.message_handler(commands=["start"])
def report(message: Message):
    splited_message = message.text.split()
    refer_id = splited_message[1] if len(splited_message) > 1 else None

    markup = InlineKeyboardMarkup()
    if refer_id:
        miniapp_button = InlineKeyboardButton(
            text="Open app",
            url=f"https://t.me/lokach_dev_bot?startapp={refer_id}",
        )
        markup.add(miniapp_button)
    else:
        miniapp_button = InlineKeyboardButton(
            text="Open app", url="https://t.me/lokach_dev_bot?startapp=lokachApp"
        )
        markup.add(miniapp_button)

    bot.send_message(message.chat.id, "Click to open app", reply_markup=markup)


if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception:
            sleep(0.3)
