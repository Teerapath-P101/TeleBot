import os
import datetime
import re
import json
import random
from cfproxy import CFProxy
from typing import NamedTuple

try:
    from pyrogram import Client
    import requests
except:
    os.system(
        "pip3 install -U https://github.com/pyrogram/pyrogram/archive/master.zip")
    os.system("pip3 install -U pyrogram tgcrypto")
    os.system("pip3 install requests")
    from pyrogram import Client
    import requests
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import PasswordRequired, YouBlockedUser, PhoneCodeInvalid, UsernameInvalid, UsernameNotOccupied, UsersTooMuch, ChannelsTooMuch, BotResponseTimeout
from pyrogram.errors.exceptions.forbidden_403 import ChatSendPollForbidden
from time import sleep
from requests.exceptions import ConnectionError

api_id = 5330210
api_hash = "a112ebb70ccee839801ef08744372fff"
#s = requests.Session()
proxy = CFProxy('my.byoi.workers.dev',
                'Mozilla/5.0 (Linux; Android 10; CPH1931) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36', '1.1.1.1')
#s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0Win64x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#user = s.headers
click_bot_username = {
    '1': ["Litecoin_click_bot", "LTC"],
    '2': ["BitcoinClick_bot", "BTC"],
    '3': ["Dogecoin_click_bot", "Doge"],
    '4': ["BCH_clickbot", "BCH"],
    '5': ['Zcash_click_bot', "ZEC"]
}
reset = '\u001b[0m'
bold = '\u001b[1m'
underline = '\u001b[4m'
B_b = '\u001b[44;1m'
B_r = '\u001b[41;1m'
r = '\u001b[31;1m'
b = '\u001b[34;1m'
cyan = '\u001b[36;1m'
g = '\u001b[32;1m'
y = '\u001b[38;5;220m'
w = '\u001b[37;1m'

if not os.path.exists(".phone_numbers_and_session_string.json"):
    with open('.phone_numbers_and_session_string.json', 'w') as w_:
        w_.write('{}')
phone_session = json.load(open('.phone_numbers_and_session_string.json', 'r'))


def menu():
    print(f"{bold}\nYour accout name: {b}{myself.first_name} {myself.last_name}{w} Your number: {b}+{myself.phone_number}{reset}")
    print(f"{bold}1) Start bot")
    print("2) Leave channel")
    print("3) Add account")
    print("4) Delete account")
    print("5) Check account")
    print(f"6) Quit{reset}")
    f = input("Enter your choice - ")
    while not main_menu.get(f):
        print(f"{r}{bold}{underline}Input invalid!{reset} Please enter again.")
        f = input("Enter your choice - ")
    return f, True


def menu_crytoCoin():
    print("\nYou can use (1/2/3/4/5) (v/m/j) for example: \n1 v (it means start LTC bot with only visit site)")
    index = " "
    f = "a"
    while (not click_bot_username.get(index)
            or f not in "vmja"):
        print("\n1) LTC\n2) BTC\n3) Doge\n4) BCH\n5) ZEC")
        index = input(f"{bold}Select the Crypto coins (To exit, press Ctrl+C+Enter) - ").lower()
        if len(index) == 3 and not index.isdigit():
            i2 = index
            index = i2[0]
            f = i2[2]
    channel_username = click_bot_username[index][0]
    try:
        client.send_message(channel_username, "/start")
    except YouBlockedUser:
        print(
            f"! {r}{bold}{underline}You have been banned... Please use another Crypto coin.{reset}")
        return menu_crytoCoin()  # if it is banned
    return channel_username, f


def check_InOrderToUseThisBot(theChannel):
    message = client.get_history(theChannel, limit=1)[0]
    if message.text.find('In order to use this bot') != -1:
        callback_data = message.reply_markup.inline_keyboard[1][0].callback_data
        url1 = message.reply_markup.inline_keyboard[0][0].url
        url2 = message.reply_markup.inline_keyboard[0][1].url
        # s.get(url1, headers=user)
        # s.get(url2, headers=user)
        proxy.get(url1)
        proxy.get(url2)
        client.request_callback_answer(
            theChannel, message.message_id, callback_data)


def phoneNumber():
    phone = input("Enter your number (with +) - ")
    while not phone.strip('+').isdigit():
        print("Invalid the phone number! Please try again")
        phone = input("Enter your number (with +) - ")
    return phone


def ChannelMember(channel, hour):
    t = datetime.datetime.now()
    with open("JoinMember.txt", 'a') as fl:
        fl.write(
            f"{channel} {(t + datetime.timedelta(hours=hour)).strftime('%X')},")


def memo_phone_numbers_and_session_string(number, session_string):
    phone_session[number] = session_string
    with open('.phone_numbers_and_session_string.json', 'w') as w_m:
        json.dump(phone_session, w_m)


def CreateClient(new_client=False):
    if new_client:
        if os.path.exists('client.session'):
            os.remove('client.session')
        client = Client("client", api_id, api_hash)
        client.start()
        phone = "+"+(client.get_me().phone_number)
        memo_phone_numbers_and_session_string(
            phone, client.export_session_string())
        return client
    else:
        client = Client(session_string, api_id, api_hash)
        client.start()
        return client


def waitforcoin(sec):
    for i in range(sec, 0, -1):
        print("\r", end="")
        print(f"{bold}Please wait {i} seconds to receive the coin ", end="")
        sleep(1)
    print(f'{reset}\r', end='')

# def callbackButton(message_id, callback_data):
#     client.request_callback_answer(channel_username, message_id, callback_data)

def visit_sites(client, channel_username):
    print(f"{bold}=========================={reset}")
    print(f"        {B_r}Vist Site{reset}")
    print(f"{bold}=========================={reset}")
    client.send_message(channel_username, "🖥 Visit sites")
    for _ in range(50):
        sleep(2)
        message = client.get_history(channel_username, limit=1)[0]
        try:
            if message.text.find("Sorry,") != -1:
                print(f"{bold}Sorry, there are no new ads available.{reset}\n")
                break
            else:
                if message.text == "Choose the reason you are reporting this ad below:":
                    client.send_message(channel_username, "❌ Cancel")
                    client.send_message(channel_username, "🖥 Visit sites")
                    sleep(1)
                    message = client.get_history(channel_username, limit=1)[0]
                message_id = message.message_id
                callback_data_SkipButton = message.reply_markup.inline_keyboard[1][1].callback_data
                url = message.reply_markup.inline_keyboard[0][0].url
                #res = s.get(url, headers=user, allow_redirects=True).text
                res = proxy.get(url).text
                if res.find("Just a moment...") != -1:
                    # client.request_callback_answer(channel_username, message_id, callback_data_SkipButton)
                    print("Cloudflare :(")
                    client.request_callback_answer(
                        channel_username, message_id, callback_data_SkipButton)
                #elif res.find('class="g-recaptcha"') != -1:
#                    print(f"{r}Skip! This Website has Captcha!{reset}")
#                    client.request_callback_answer(
#                        channel_username, message_id, callback_data_SkipButton)
                elif res.find('class="container-fluid"') != -1:
                    try:
                        data = re.findall(
                            'class="container-fluid" (.*) data-curr=', res)[0].split()
                    except:
                        continue
                    timer = data[1].split('=')[1].strip('"')
                    code = data[0].split('=')[1].strip('"')
                    token = data[2].split('=')[1].strip('"')
                    waitforcoin(int(timer))
                    proxy.post("https://dogeclick.com/reward",
                               data={"code": code, "token": token})
                    sleep(2)
                    message_reward = client.get_history(channel_username, limit=2)[1].text
                    print(f"{y}[{g}✓{y}] {message_reward}{reset}")
                else:
                    timer = client.get_history(channel_username, limit=1)[0].text.split()[-2]
                    waitforcoin(int(timer))
                    sleep(2)
                    message_reward = client.get_history(
                        channel_username, limit=2)[1].text
                    print(f"{y}[{g}✓{y}] {message_reward}{reset}")
        except:
            client.send_message(channel_username, "🖥 Visit sites")

def message_bots(client, channel_username):
    print(f"{bold}=========================={reset}")
    print(f"        {B_r}Message Bot{reset}")
    print(f"{bold}=========================={reset}")
    client.send_message(channel_username, "🤖 Message bots")
    for _ in range(50):
        sleep(2)
        message = client.get_history(channel_username, limit=1)[0]
        try:
            if message.text.find("Sorry,") != -1:
                print(f"{bold}Sorry, there are no new ads available.{reset}\n")
                break
            else:
                if message.text == "Choose the reason you are reporting this ad below:":
                    client.send_message(channel_username, "❌ Cancel")
                    client.send_message(channel_username, "🤖 Message bots")
                    sleep(1)
                    message = client.get_history(channel_username, limit=1)[0]
                message_id = message.message_id
                callback_data_SkipButton = message.reply_markup.inline_keyboard[1][1].callback_data
                url = message.reply_markup.inline_keyboard[0][0].url
                res = proxy.get(url).text
                if res.find("Just a moment...") != -1:
                    print("Cloudflare :(")
                    client.request_callback_answer(
                        channel_username, message_id, callback_data_SkipButton)
                else:
                    name_bot = re.findall(
                        '<title>Telegram: Contact (.*)</title>', res)[0]
                    client.send_message(name_bot, "/start")
                    sleep(2)
                    message = client.get_history(name_bot, limit=1)[0]
                    c = 0
                    while message.text == "/start" and c != 30:
                        sleep(1)
                        c += 1
                        message = client.get_history(name_bot, limit=1)[0]
                    client.forward_messages(
                        channel_username, name_bot, message.message_id)
                    sleep(2)
                    post = client.get_history(channel_username)[0]
                    if post.text.split('\n\n')[0] == "Sorry, that is not a valid forwarded message.":
                        print(f"{r}Skip! This chat bot is not responding.{reset}")
                        client.request_callback_answer(
                            channel_username, message_id, callback_data_SkipButton)
                    else:
                        reward = client.get_history(
                            channel_username, limit=2)[1].text
                        print(f"{y}[{g}✓{y}] {reward}{reset}")
        except ConnectionError:
            continue

def join_chats(client, channel_username):
    print(f"\n{bold}=========================={reset}")
    print(f"        {B_r}Join Chats{reset}")
    print(f"{bold}=========================={reset}")
    client.send_message(channel_username, "📣 Join chats")
    a = 0
    for _ in range(50):
        sleep(2)
        message = client.get_history(channel_username, limit=1)[0]
        try:
            if message.text.find("Sorry,") != -1:
                if a == 2:
                    print(f"{bold}Sorry, there are no new ads available.{reset}\n")
                    break
                else:
                    client.send_message(channel_username, "📣 Join chats")
                    sleep(2)
                    message = client.get_history(channel_username, limit=1)[0]
            else:
                if message.text == "Choose the reason you are reporting this ad below:":
                    client.send_message(channel_username, "❌ Cancel")
                    client.send_message(channel_username, "📣 Join chats")
                    sleep(1)
                    message = client.get_history(channel_username, limit=1)[0]
                message_id = message.message_id
                callback_data_SkipButton = message.reply_markup.inline_keyboard[1][1].callback_data
                callback_data_JoinedButton = message.reply_markup.inline_keyboard[0][1].callback_data
                url = message.reply_markup.inline_keyboard[0][0].url
                res = proxy.get(url).text
                if res.find("Just a moment...") != -1:
                    print("Cloudflare :(")
                    client.request_callback_answer(
                        channel_username, message_id, callback_data_SkipButton)
                else:
                    ch_name = re.findall(
                        r'<title>Telegram: Contact (.*)</title>', res)[0]
                    try:
                        client.join_chat(ch_name)
                    except FloodWait:
                        for t in range(280, 0, -1):
                            print("\r", end="")
                            print(
                                f'{bold}A wait of {t} seconds is required{reset}', end="")
                            sleep(1)
                        print('\r', end='')
                        continue
                    except (UsernameInvalid, UsernameNotOccupied):
                        print(f"{bold}This username is invalid. Skip!{reset}")
                        client.request_callback_answer(
                            channel_username, message_id, callback_data_SkipButton)
                        continue
                    except ChannelsTooMuch:
                        print(f"{bold}Skip! This group is full.{reset}")
                        client.request_callback_answer(
                            channel_username, message_id, callback_data_SkipButton)
                        continue
                    except BotResponseTimeout:
                        print(f"{bold}Skip! Servers of this group are low.{reset}")
                        try:
                            client.request_callback_answer(
                                channel_username, message_id, callback_data_SkipButton)
                        except:
                            sleep(3)
                            client.request_callback_answer(
                                channel_username, message_id, callback_data_SkipButton)
                    except UsersTooMuch:
                        print(
                            f"{r}Join Error!{reset}\nYou are a member of too many channel! Please use {bold}'Leave Channel' function {reset}")
                        break
                    sleep(1)
                    client.request_callback_answer(
                        channel_username, message_id, callback_data_JoinedButton)
                    sleep(2)
                    message = client.get_history(channel_username, limit=1)[0]
                    if message.text.find("Success! 👍") != -1:
                        reward = message.text.split('\n')[1:]
                        print(f"{y}[{g}✓{y}] {reward}{reset}")
                        client.send_message(channel_username, "📣 Join chats")
                    elif message.text.find("WARNING") != -1:
                        reward = '\n'.join(
                            (client.get_history(channel_username, limit=2)[1].text.split('\n')[1:]))
                        print(f"{y}[{g}✓{y}] {reward}{reset}")
        except ConnectionError:
            pass

def start():
    try:
        result = menu_crytoCoin()
        channel_username, f = result
        for i, client in enumerate(clients):
            me = client.get_me()
            print(f"{bold}It will run all accounts! (There are {len(clients)}){reset}")
            print(f"\n{bold}{i+1}. {cyan}{me.first_name} {me.last_name} {w}({cyan}+{me.phone_number}{w}){reset}")
            check_InOrderToUseThisBot(channel_username)
            print(f"{bold}To exit, press Ctrl+C{reset}")
            funcs = {'v': [visit_sites], 'm': [message_bots], 'j': [
                join_chats], 'a': [visit_sites, message_bots, join_chats]}
            for func in funcs[f]:
                func(client, channel_username)
        print("\n\n")
    except KeyboardInterrupt:
        pass

def leave():
    print(f"\n\n{bold}=========================={reset}")
    print(f"      {B_b}Leave Channel{reset}")
    print(f"{bold}=========================={reset}\n")
    for i, cli in enumerate(clients):
        amount = 0
        me = cli.get_me()
        print(f"\u001b[38;5;It will run all accounts! (There are {len(clients)}){reset}")
        print(f"\n{bold}{i+1}. {cyan}{me.first_name} {me.last_name} {w}({cyan}+{me.phone_number}{w}){reset}")
        for ch in cli.get_dialogs(limit=500):
            try:
                chat = ch.chat
                if chat.title != None:
                    print(f"{bold}{chat.title}  {g}Leave Success{reset}")
                    cli.leave_chat(chat.id)
                    amount += 1
                else:
                    continue
            except:
                pass
        print(f"\n{y}[{g}✓{y}] Leave Successful!{reset}")
        print(f"{bold}{underline}Total Channel: {amount}{reset}")
        print('------------------------------------------\n\n')

def add():
    global phone_session, clients
    #phone = phoneNumber()
    sure = input("Are you sure? (y/n) - ").lower()
    if sure == "y":
        cli = CreateClient(new_client=True)
        me = cli.get_me()
        print(
            f"\n\n\n{g}{bold}Your account has now been added! ({me.first_name} {me.last_name}){reset}")
        clients.append(cli)
        phone_session = json.load(
            open('.phone_numbers_and_session_string.json', 'r'))

def delete():
    global phone_session
    phone_keys = list(phone_session)
    if len(phone_keys) == 1:
        print(f"{r}{bold}{underline}Warning! You only have 1 account, if you delete it, it will be exit.{reset}")
    try:
        for i, cli in enumerate(clients):
            me = cli.get_me()
            print(
                f"{i+1}) {cyan}{me.first_name} {me.last_name} {w}({cyan}+{me.phone_number}{w})")
        k = int(input("Enter your choice to delete (To exit, press Ctrl+C+Enter) - "))-1
        while not phone_session.get(phone_keys[k]):
            print(f"{r}Invaild! Please try again{reset}")
            k = int(input("Enter your choice to delete"))-1
        clients[k].terminate()
        del phone_session[phone_keys[k]], clients[k]
        print(f"{g}{bold}Delete Success!{reset}")
        if len(clients)==0: exit()
    except KeyboardInterrupt:
        pass
    
def check_acc():
    print(bold+"There are", len(clients))
    for cli in clients:
        me = cli.get_me()
        print(
            f"    {cyan}{me.first_name} {me.last_name} {w}({cyan}+{me.phone_number}{w})")

def Quit():
	try:
	   for cli in clients:
	   	cli.terminate()
	except:
	   pass
	print(f"{g}{bold}Bye Bye, See you again Thanks for using this bot :), Good luck{reset}")
	quit()

if phone_session == {}:
    #phone = phoneNumber()
    clients = [CreateClient(new_client=True)]
    client = clients[0]
    myself = client.get_me()
else:
    clients = []
    for phone in phone_session:
        session_string = phone_session[phone]
        clients.append(CreateClient())
    client = clients[0]
    myself = client.get_me()
    #phone = '+'+myself.phone_number
os.system('cls' if os.name == 'nt' else 'clear')

main_menu = {"1": start, "2": leave, "3": add,
             "4": delete, "5": check_acc, "6": Quit}
banner1 = f"""
{bold}{r}████████╗ █████╗ ███████╗     
{reset}╚══██╔══╝██╔══██╗██╔════╝         
   {b}██║   ███████║█████╗ {reset}          
   ██║   ██╔══██║██╔══╝           
   {r}██║   ██║  ██║███████╗██╗██╗██╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚═╝╚═╝{reset}
                                  """
banner2 = f"""
 {r} _________    ______   
 /_  __/   |  / ____/{reset}   
  / / / /| | / __/      
 {b}/ / / ___ |/ /____ _ _{reset} 
/_/ /_/  |_/_____(_|_|_)
                        
"""
banner = random.choice([banner1, banner2])
print(banner)
print('-------------------------------------------')
print(f"{bold}Welcome to Tele-Bot {myself.first_name}! You can choose the functions below!")
menu_Chossed = menu()
while menu_Chossed[1]:
    print("\n")
    main_menu[menu_Chossed[0]]()
    menu_Chossed = menu()
