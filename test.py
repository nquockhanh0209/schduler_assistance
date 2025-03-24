
# bot = TeleBot("7499935883:AAFlo8OPnPWeFbrVUwthNh8P774jUsFQZsY")
# # chat_id = bot.get_chat()
# # ("@khanhv0209")
# bot.send_message(chat_id=5569919949, text="khanhv0209")
from datetime import time
import datetime
import pandas as pd
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
TOKEN = "7002033625:AAFgDBVBuVJ2jlXdvUawUrPLE6RGoeaf5kM"
bot = telebot.TeleBot(TOKEN)
import base64
@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup()
    button = InlineKeyboardButton("Click Me!", callback_data="change_text|123")
    markup.add(button)
    bot.send_message(message.chat.id, "Click the button below:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("change_text"))
def callback_query(call):
    # Extract data
    _, task_id = call.data.split("|")  # Splitting the callback_data

    # Create a new markup with the updated button text
    new_markup = InlineKeyboardMarkup()
    updated_button = InlineKeyboardButton(f"Task {task_id} Clicked!", callback_data=f"changed|{task_id}")
    new_markup.add(updated_button)

    # Edit the button text dynamically
    bot.edit_message_reply_markup(chat_id=call.message.chat.id, 
                                  message_id=call.message.message_id, 
                                  reply_markup=new_markup)

bot.polling()