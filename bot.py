import os, datetime, re, json
from cfproxy import CFProxy
from typing import NamedTuple

try:
    from pyrogram import Client
    import requests
except:
    os.system("pip3 install -U https://github.com/pyrogram/pyrogram/archive/master.zip")
    os.system("pip3 install -U pyrogram tgcrypto")
    os.system("pip3 install requests")
    from pyrogram import Client
    import requests
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import PasswordRequired, YouBlockedUser, PhoneCodeInvalid
from pyrogram.errors.exceptions.forbidden_403 import ChatSendPollForbidden
from time import sleep
from requests.exceptions import ConnectionError

api_id= 5330210
api_hash= "a112ebb70ccee839801ef08744372fff"
#s = requests.Session()
proxy = CFProxy('my.byoi.workers.dev', 'Mozilla/5.0 (Linux; Android 10; CPH1931) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Mobile Safari/537.36', '1.1.1.1')
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
    print(f"{bold}\nYour accout name: {b}{myself.first_name} {myself.last_name}{w} Your number: {b}{myself.phone_number}{reset}")
    print(f"{bold}1) Start bot")
    print("2) Leave channel")
    print("3) Add number")
    print("4) Check account")
    print("5) Check all balances")
    print(f"6) Quit{reset}")
    a = input("Enter your choice - ")
    while len(a) != 1 or a not in '123456':
        print(f"{r}{bold}{underline}Input invalid!{reset} Please enter again.")
        a = input("Enter your choice - ")
    if a == '6':
        try:
            for cli in clients:
                cli.terminate()
        except:
            pass
        print(
            f"{g}{bold}Bye Bye, See you again Thanks for using this bot :), Good luck{reset}")
        quit()
    return a, True

def menu_crytoCoin():
    index = " "
    f = "a"
    while (len(index)!=1 or index not in '12345' 
            or f not in "vmja"):
        print("\n\n1) LTC\n2) BTC\n3) Doge\n4) BCH\n")
        index = input("Select the Crypto coins - ").lower()
        if len(index)==3 and not index.isdigit():
        	i2 = index
        	index = i2[0]
        	f = i2[2]
    channel_username = click_bot_username[int(index)-1][0]
    try:
        client.send_message(channel_username, "/start")
    except YouBlockedUser:
        print(f"! {r}{bold}{underline}You have been banned... Please use another Crypto coin.{reset}")
        return menu_crytoCoin()  #if it is banned
    return channel_username

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
        client.request_callback_answer(theChannel, message.message_id, callback_data)

def phoneNumber():
    phone = input("Enter your number (with +) - ")
    while not phone.strip('+').isdigit():
        print("Invalid the phone number! Please try again")
        phone = input("Enter your number (with +) - ")
    return phone

def ChannelMember(channel, hour):
    t = datetime.datetime.now()
    with open("JoinMember.txt", 'a') as f:
        f.write(
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
        #client.connect()
        # try:
        #     code = client.send_code(phone)
        #     client.sign_in(phone, code.phone_code_hash, input("Enter your verification code - "))
        # except PhoneCodeInvalid:
        #     print('Wrong code! I will send you a new code. Please try again')
        #     code = client.send_code(phone)
        #     client.sign_in(phone, code.phone_code_hash, input("Enter your verification code - "))
        # except FloodWait as s:
        #     h = divmod(s.seconds/60, 1)[0]//60
        #     print(f"Sorry, Please try again after {int(h)} hours.")
        #     exit()
        client.start()
        phone = client.get_me().phone_number
        memo_phone_numbers_and_session_string(phone, client.export_session_string())
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

def visit_sites():
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
                    print(res.text, f"\n\n{r}Fix{reset}")
                elif res.find('class="g-recaptcha"') != -1:
                    print(f"{r}Skip! This Website has Captcha!{reset}")
                    client.request_callback_answer(channel_username, message_id, callback_data_SkipButton)
                elif res.find('class="container-fluid"') != -1:
                    try:
                        data = re.findall('class="container-fluid" (.*) data-curr=', res)[0].split()
                    except:
                        continue
                    timer = data[1].split('=')[1].strip('"')
                    code = data[0].split('=')[1].strip('"')
                    token = data[2].split('=')[1].strip('"')
                    waitforcoin(int(timer))
                    proxy.post("https://dogeclick.com/reward", data={"code": code, "token": token})
                    sleep(2)
                    message_reward = client.get_history(channel_username, limit=2)[1].text
                    print(f"{y}[{g}✓{y}] {message_reward}{reset}")
                else:
                    timer = client.get_history(channel_username, limit=1)[0].text.split()[-2]
                    waitforcoin(int(timer))
                    sleep(2)
                    message_reward = client.get_history(channel_username, limit=2)[1].text
                    print(f"{y}[{g}✓{y}] {message_reward}{reset}")
        except:
            client.send_message(channel_username, "🖥 Visit sites")

def message_bots():
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
                    print(res.text, f"\n\n{r}Fix{reset}")
                else:
                    name_bot = re.findall('<title>Telegram: Contact (.*)</title>', res)[0]
                    client.send_message(name_bot, "/start")
                    sleep(2)
                    message = client.get_history(name_bot, limit=1)[0]
                    c = 0
                    while message.text == "/start" and c != 30:
                        sleep(1)
                        c += 1
                        message = client.get_history(name_bot, limit=1)[0]
                    client.forward_messages(channel_username, name_bot, message.message_id)
                    sleep(2)
                    post = client.get_history(channel_username)[0]
                    if post.text.split('\n\n')[0] == "Sorry, that is not a valid forwarded message.":
                        print(f"{r}Skip! This chat bot is not responding.{reset}")
                        client.request_callback_answer(channel_username, message_id, callback_data_SkipButton)
                    else:
                        reward = client.get_history(channel_username, limit=2)[1].text
                        print(f"{y}[{g}✓{y}] {reward}{reset}")
        except ConnectionError:
            continue

def join_chats():
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
                if a==2:
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
                    print(res.text, f"\n\n{r}Fix{reset}")
                else:
                    ch_name = re.findall(r'<title>Telegram: Contact (.*)</title>', res)[0]
                    try:
                        client.join_chat(ch_name)
                    except FloodWait:
                        for t in range(280, 0, -1):
                            print("\r", end="")
                            print(f'{bold}A wait of {t} seconds is required (caused by "channels.JoinChannel"){reset}', end="")
                            sleep(1)
                        print('\r', end='')
                        continue
                    # except UsersTooMuchError:
                    #     print(f"{r}Skip! This group is full.{reset}")
                    #     callbackButton(message_id, callback_data_SkipButton)
                    #     continue
                    # except BotResponseTimeoutError:
                    #     print(f"{r}Skip! Servers of this group are low.{reset}")
                    #     callbackButton(message_id, callback_data_SkipButton)
                    # except FloodWait:
                    #     print(f"{bold}A wait of 207 seconds is required (caused by JoinChannelRequest){reset}")
                    #     sleep(210)
                    #     continue
                    # except:
                    #     print(f"{r}Join Error!{reset}\nYou are a member of too many channel! Please use {bold}'Leave Channel' function {reset}")
                    #     break
                    client.request_callback_answer(channel_username, message_id, callback_data_JoinedButton)
                    message = client.get_history(channel_username, limit=1)[0]
                    sleep(2)
                    if message.text.find("Sorry,") != -1:
                        continue
                    elif message.text.find("Success! 👍") != -1:
                        reward = "\n".join(client.get_history(channel_username, limit=1)[0].text.split('\n')[1:])
                        print(f"{y}[{g}✓{y}] {reward}{reset}")
                        client.send_message(channel_username, "📣 Join chats")
                    else:
                        reward = '\n'.join((client.get_history(channel_username, limit=2)[1].text.split('\n')[1:]))
                        print(f"{y}[{g}✓{y}] {reward}{reset}")
        except ConnectionError:
            pass

if phone_session == {}:
    #phone = phoneNumber()
    clients = [CreateClient(new_client=True)]
    client = clients[0]
    myself = client.get_me()
    #phone = "+"+myself.phone_number
else:
    clients = []
    for phone in phone_session:
        session_string = phone_session[phone]
        clients.append(CreateClient())
    client = clients[0]
    myself = client.get_me()
    #phone = '+'+myself.phone_number
os.system('cls' if os.name=='nt' else 'clear')

banned1 = """████████╗ █████╗ ███████╗         
╚══██╔══╝██╔══██╗██╔════╝         
   ██║   ███████║█████╗           
   ██║   ██╔══██║██╔══╝           
   ██║   ██║  ██║███████╗██╗██╗██╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚═╝╚═╝
                                  """
banned2 = """ _________     _       ________           
|  _   _  |   / \     |_   __  |          
|_/ | | \_|  / _ \      | |_ \_|          
    | |     / ___ \     |  _| _           
   _| |_  _/ /   \ \_  _| |__/ | _  _  _  
  |_____||____| |____||________|(_)(_)(_) 
                                          """
print(f"""\n{b}{banned1}{reset}\n""")
print('-------------------------------------------')
print(f"{bold}Welcome to Tele-Bot {myself.first_name}! You can choose the functions below!")
menu_Chossed = menu()
while menu_Chossed[1]:
    if menu_Chossed[0] == '1':
        channel_username = menu_crytoCoin()
        for i, client in enumerate(clients):
            myself = client.get_me()
            print(f"{bold}It will run all accounts! (There are {len(clients)}){reset}")
            print(f"\n{bold}{i+1}. {cyan}{myself.first_name} {myself.last_name} {w}({cyan}+{myself.phone_number}{w}){reset}")
            check_InOrderToUseThisBot(channel_username)
            visit_sites()
            
            message_bots()
            
            join_chats()
        print("\n\n")
        menu_Chossed = menu()

    elif menu_Chossed[0] == '2':
        print(f"\n\n{bold}=========================={reset}")
        print(f"      {B_b}Leave Channel{reset}")
        print(f"{bold}=========================={reset}\n")
        for client in clients:
            amount = 0
            myself = client.get_me()
            print(f"\u001b[38;5;It will run all accounts! (There are {len(clients)}){reset}")
            print(f"\n{bold}{i+1}. {cyan}{myself.first_name} {myself.last_name} {w}({cyan}+{myself.phone_number}{w}){reset}")
            for ch in client.get_dialogs(limit=500):
                try:
                    chat = ch.chat
                    if chat.title != None:
                        print(f"{bold}{chat.title}  {g}Leave Success{reset}")
                        client.leave_chat(chat.id)
                        amount += 1
                    else:
                        continue
                except:
                    pass
            print(f"\n{y}[{g}✓{y}] Leave Successfully!{reset}")
            print(f"{bold}{underline}Total Channel: {amount}{reset}")
            print('------------------------------------------\n\n')
        menu_Chossed = menu()
    
    elif menu_Chossed[0] == '3':
        #phone = phoneNumber()
        sure = input("Are you sure? (y/n) - ").lower()
        if sure == "y":
            cli = CreateClient(new_client=True)
            me = cli.get_me()
            print(f"\n\n\n{g}{bold}Your account has now been added! ({me.first_name} {me.last_name}){reset}")
            clients.append(cli)
            phone_session = json.load(open('.phone_numbers_and_session_string.json', 'r'))
        menu_Chossed = menu()
        
    elif menu_Chossed[0] == '4':
    	menu_Chossed = menu()
    	
    elif menu_Chossed[0] == '5':
        print(bold+"There are", len(clients))
        for cli in clients:
            me = cli.get_me()
            print(f"    {cyan}{me.first_name} {me.last_name} {w}({cyan}+{me.phone_number}{w})")
        menu_Chossed = menu()
       
    elif menu_Chossed[0] == '6':
        print(f"\n{bold}You have {len(clients)} account:")
        print("Please, wait...")
        clients_balance = {}
        for client in clients:
            me = client.get_me()
            phone = "+"+me.phone_number
            balances = {"LTC": 0, "BTC": 0, "Doge": 0, "BCH": 0, "ZEC": 0}
            cli = f"{me.first_name} {me.last_name} ({phone})"
            for index in click_bot_username:
                name = click_bot_username[index][0]
                name2 = click_bot_username[index][1]
                try:
                    client.send_message(name, "💰 Balance")
                    sleep(2)
                    check_InOrderToUseThisBot(name)
                    if client.get_history(name, limit=1)[0].text.find("Welcome to") != -1:
                        client.send_message(name, "💰 Balance")
                        sleep(2)
                    balances[name2] = client.get_history(name, limit=1)[0].text
                except YouBlockedUser:
                    balances[name2] = "Banned"
            clients_balance[cli] = balances
        print("\r", end="")
        for i, c in enumerate(clients_balance):
            print(f"{bold}{i+1}. {cyan}{c}{reset}")
            balances = clients_balance[c]
            for balance in balances:
                if balances[balance] == "Banned":
                    print(f"    {b}{balance} balances: {r}Banned")
                else:
                    print(f"    {b}{balance} balances: {y}{balances[balance]}")
        print('------------------------------------------\n')
        menu_Chossed = menu()

"""
ทำที่เลือกแบบใหม่ เป็น dict
เพิ่ม funcion Delete account
quit เป็นบรรทัยสุดท้ายแทนที่อยู่ใน menu()
Error pyrogram.errors.exceptions.bad_request_400.UsernameInvalid: [400 USERNAME_INVALID]: The username is invalid (caused by "contacts.ResolveUsername")
Photo in phone
"""
