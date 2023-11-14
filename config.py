import os
from betterconf import Config, field
from betterconf.config import AbstractProvider
import telebot

import  json

from colorama import init, Fore, Style, Back

from banner import banner

from configparser import ConfigParser, NoSectionError, NoOptionError

init()

# Определение цветов
red = Fore.RED
cyan = Fore.CYAN
blue = Fore.BLUE
green = Fore.GREEN

yellow = Fore.YELLOW
reset = Style.RESET_ALL
bold = Style.BRIGHT

def is_valid_token(token) -> bool:

    try:
        bot = telebot.TeleBot(token)
        bot_info = bot.get_me()
        if bot_info:
            return True
    except telebot.apihelper.ApiException:
        return False
    
def update_data(key: str, value):
    with open('config.json') as f:
        data = json.load(f)
    data[key] = value
    with open("config.json", "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.close()

def cfg() -> ConfigParser:
    conf = ConfigParser()
    conf.read("./config.ini")
    return conf

def cfg_commit(conf: ConfigParser) -> None:
    with open('./config.ini', "w") as f:
        conf.write(f)

class Config:
    def __init__(self, proj) -> None:
        conf = cfg()
        self.main(conf, proj)

    def main(self, conf, proj):
        try:
            self.title = conf.get(proj, "title") if conf.get(proj, "title") != "" else input(f"     {blue}Введите название проекта >> ")
        except NoSectionError:
            conf.add_section(proj)
            self.title = input(f"     {blue}Введите название проекта >> ")
            conf.set(proj, 'title', self.title)
        except NoOptionError:
            self.title = input(f"     {blue}Введите название проекта >> ")
            conf.set(proj, 'title', self.title)
        try:
            self.token = conf.get(proj, "token") if conf.get(proj, "token") != "" else input(f"     {blue}Введите токен вашего бота >> ")
        except NoOptionError:
            self.token = input(f"     {blue}Введите токен вашего бота >> ")
            conf.set(proj, 'token', self.token)

        try:
            self.admin = conf.get(proj, "admin") if conf.get(proj, "admin") != "" else input(f"     {blue}Введите ваш телеграм айди >> ")
        except NoOptionError:
            self.admin = input(f"     {blue}Введите ваш телеграм айди >> ")
            conf.set(proj, 'admin', self.admin)

        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner.format(bold=bold, blue=blue, reset=reset, title=self.title, yellow=yellow, cyan=cyan))
        if not is_valid_token(self.token):
            exist = False
            while exist != True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner.format(bold=bold, blue=blue, reset=reset, title=self.title, yellow=yellow, cyan=cyan))
                self.token = input(f"     {blue}Введите токен вашего бота >> ")
                if is_valid_token(self.token):
                    conf.set(proj, 'token', self.token)
                    exist = True
        if not self.admin.isnumeric():
            exist = False
            while exist != True:
                os.system('cls' if os.name == 'nt' else 'clear')
                print(banner.format(bold=bold, blue=blue, reset=reset, title=self.title, yellow=yellow, cyan=cyan))
                print(f"     {blue}Введите токен вашего бота >> {self.token}")
                self.admin = input(f"     {blue}Введите ваш телеграм айди >> ")
                if self.admin.isnumeric():
                    conf.set(proj, 'admin', self.admin)
                    exist = True
        cfg_commit(conf)