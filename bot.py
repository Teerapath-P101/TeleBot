from telethon import TelegramClient, sync
from telethon.tl.functions.channels import *
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from telethon.errors import FloodWaitError, PhoneCodeInvalidError, BotResponseTimeoutError
from telethon.errors.rpcerrorlist import UsersTooMuchError
from time import sleep
import os, sys, requests, datetime, re
from requests.exceptions import ConnectionError

if not os.path.exists("session"):
    os.makedirs("session")
s = requests.Session()

reset = '\u001b[0m'
bold = '\u001b[1m'
underline = '\u001b[4m'
B_b = '\u001b[44;1m'
B_r = '\u001b[41;1m'
r = '\u001b[31;1m'
b = '\u001b[34;1m'
g = '\u001b[32;1m'
y = '\u001b[38;5;220m'
w = '\u001b[37;1m'

def menu():
    print(f"{bold}\nYour accout name: {myself.first_name} {myself.last_name}  Your number:  +{myself.phone}")
    print(f"1) Start bot")
    print("2) Leave channel")
    print("3) Add number")
    print(f"4) Quit{reset}")
    a = input("Enter your choice - ")
    while len(a) != 1 or a not in '1234':
        print(f"{r}{bold}{underline}Input invalid!{reset} Please enter again.")
        a = input("Enter your choice - ")
    if a == '4':
        print(f"{g}{bold}Bye Bye, See you again Thanks for using this bot :), Good luck{reset}")
        quit()
    return a

def check_InOrderIoUseThisBot():
    mess = client.get_messages(channel_entity.username)
    id = mess[0].id
    if mess[0].message == 'In order to use this bot, you must agree to our Terms of Service and Privacy Policy.\n\nPlease read our Terms of Service and Privacy Policy, then press the button below to move forward.':
        url1 = mess[0].reply_markup.rows[0].buttons[0].url
        url2 = mess[0].reply_markup.rows[0].buttons[1].url
        s.get(
            url1,
            headers=user,
            timeout=10,
            allow_redirects=True
        )
        s.get(
            url2,
            headers=user,
            timeout=10,
            allow_redirects=True
        )
        client(
            GetBotCallbackAnswerRequest(
                channel_entity,
                id,
                data=mess[0].reply_markup.rows[1].buttons[0].data,
            )
        )

def wait(sec):
    for i in range(sec, 0, -1):
        print("\r", end="")
        print(f"Please wait {i} seconds to receive the coin  ", end="")
        sleep(1)
    print('\r',end='')

def skipTask(_data, _id):
    client(
        GetBotCallbackAnswerRequest(
            peer= channel_entity.username,
            msg_id= _id,
            data= _data
        )
    )

def vist_site():
    global g, y, w, r, reset
    client.send_message(channel_entity.username, "🖥 Visit sites")
    sleep(1)
    mess = client.get_messages(channel_entity.username)[0]

    if mess.message == "🖥 Visit sites":
        client.send_message(channel_entity.username, "🖥 Visit sites")
        print("! Server Bot is low")
        while mess == "🖥 Visit sites":
            mess = client.get_messages(channel_entity.username)[0]

    for _ in range(50):
        sleep(1)
        mess = client.get_messages(channel_entity.username)[0]
        try:
            if mess.message.split("\n\n")[0] == "Sorry, there are no new ads available. 😟":
                print("Sorry, there are no new ads available")
                break
            else:
                _id = mess.id
                sleep(1)
                try:
                    url = mess.reply_markup.rows[0].buttons[0].url.strip().strip("'").strip('"')
                except:
                    sleep(7)
                    mess = client.get_messages(channel_entity.username)[0]
                    try:
                        url = mess.reply_markup.rows[0].buttons[0].url.strip().strip("'").strip('"')
                    except:
                        sleep(3)
                        mess = client.get_messages(channel_entity.username)[0]
                        url = mess.reply_markup.rows[0].buttons[0].url.strip().strip("'").strip('"')
                res = s.get(
                    url,
                    headers=user,
                    timeout=10,
                    allow_redirects=True
                ).text
                if res.find("Just a moment...") != -1:
                    print(f"{r}Skip Checking your browser before accessing{reset}")
                    try:
                        skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                    except:
                        print(mess)
                elif res.find('class="g-recaptcha"') != -1:
                    print(f"{r}Skip! This Website has Captcha!{reset}")
                    skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                elif res.find('class="container-fluid"') != -1:
                    try:
                        data = re.findall('class="container-fluid" (.*) data-curr=', res)[0].split()
                    except:
                        continue
                    timer = data[1].split('=')[1].strip('"')
                    code = data[0].split('=')[1].strip('"')
                    token = data[2].split('=')[1].strip('"')
                    wait(int(timer))
                    try:
                        post = s.post("https://dogeclick.com/reward",
                                    data={"code": code, "token": token}, headers=user).json()
                    except:
                        post = s.post("https://dogeclick.com/reward",
                                    data={"code": code, "token": token}, headers=user).json()
                    print(
                        f"{y}[{g}✓{y}] You earned {post['reward']} the coin for visiting a site!{reset}\n")
                else:
                    post = client.get_messages(channel_entity.username)
                    wait(int(post[0].message.split()[-2]))
                    sleep(1)
                    post = client.get_messages(channel_entity.username, limit=2)[1].message
                    print(
                        f"{y}[{g}✓{y}] {post}{reset}")
        except ConnectionError:
            continue
def message_bot():
    global g, y, w, r, reset
    client.send_message(channel_entity.username, "🤖 Message bots")
    sleep(1)
    mess = client.get_messages(channel_entity.username)[0]
    if mess == "🤖 Message bots":
        client.send_message(channel_entity.username, "🤖 Message bots")
        print(f"{r}! Server Bot is low{reset}")
        while mess == "🤖 Message bots":
            mess = client.get_messages(channel_entity.username)[0]
    for _ in range(60):
        try:
            mess = client.get_messages(channel_entity.username)[0]
            if mess.message.split('\n\n')[0] == 'Sorry, there are no new ads available. 😟':
                print(f"{bold}Sorry, there are no new ads available.{reset}")
                break
            else:
                sleep(1)
                _id = mess.id
                
                url = mess.reply_markup.rows[0].buttons[0].url
                res = s.get(
                    url,
                    headers=user,
                    timeout=10,
                    allow_redirects=True
                ).text
                if res.find("Just a moment...") != -1:
                    print(f"{r}Skip Checking your browser before accessing{reset}")
                    skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                else:
                    name_chat = re.findall('<title>Telegram: Contact (.*)</title>', res)[0]
                    botChat_entity = client.get_entity(name_chat)
                    client.send_message(botChat_entity, "/start")
                    sleep(2)
                    mess_bot = client.get_messages(botChat_entity)
                    c = 0
                    while mess_bot[0].message == "/start" and c != 60:
                        sleep(1)
                        mess_bot = client.get_messages(botChat_entity)
                        c += 1
                    client.forward_messages(
                        channel_entity.username,
                        mess_bot,
                        botChat_entity
                    )
                    sleep(1)
                    post = client.get_messages(channel_entity.username)[0]
                    if post.message.split('\n\n')[0] == "Sorry, that is not a valid forwarded message.":
                        print(
                            f"{r}Skip! This chat bot is not responding.{reset}")
                        mess = client.get_messages(channel_entity.username, limit=3)[2]
                        skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                    else:
                        post = client.get_messages(channel_entity.username, limit=2)[1].message
                        print(
                            f"{y}[{g}✓{y}] {post}{reset}")
        except ConnectionError:
            continue
def join_chats():
    global g, y, w, r, reset
    client.send_message(channel_entity.username, "📣 Join chats")
    a = 0
    sleep(1)
    mess = client.get_messages(channel_entity.username)[0]

    if mess.message == "📣 Join chats":
        client.send_message(channel_entity.username, "📣 Join chats")
        print("! Server Bot is low")
        while mess == "📣 Join chats":
            mess = client.get_messages(channel_entity.username)[0]

    for _ in range(40):
            sleep(2)
            mess = client.get_messages(channel_entity.username)[0]
            _id = mess.id
            try:
                if mess.message == 'Sorry, that task is no longer valid. 😟\n\nUse/join to get a new one.':
                    if a == 2:
                        print("[\u001b[38;5;1m!] " +
                            "Sorry, that task is no longer valid."+"")
                        break
                    client.send_message(channel_entity.username, "/join")
                    a += 1
                else:
                    url = mess.reply_markup.rows[0].buttons[0].url
                    res = s.get(
                        url,
                        headers=user,
                        timeout=10,
                        allow_redirects=True
                    ).text
                    if res.find("Just a moment...") != -1:
                        print(
                            f"{r}Skip Checking your browser before accessing{reset}")
                        skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                    else:
                        ch_name = re.findall(r'<title>Telegram: Contact (.*)</title>', res)[0]
                        try:
                            chat_entity = client.get_entity(ch_name)
                        except:
                            print(
                                f"{r}Skip! There is no Telegram account with this username.{reset}")
                            skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                            continue
                        try:
                            client(JoinChannelRequest(chat_entity.username))
                        except UsersTooMuchError:
                            print(f"{r}Skip! This group is full.{reset}")
                            skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                            continue
                        except BotResponseTimeoutError:
                            print(f"{r}Skip! Servers of this group are low.{reset}")
                            skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                        except FloodWaitError:
                            print(
                                f"{bold}A wait of 207 seconds is required (caused by JoinChannelRequest){reset}")
                            wait(int(210))
                            continue
                        except:
                            print(
                                f"{r}Join Error!{reset}\nYou are a member of too many channel! Please use function {bold}'Leave Channel'{reset}")
                            break

                        client(
                            GetBotCallbackAnswerRequest(
                                peer=channel_entity.username,
                                msg_id=_id,
                                data=mess.reply_markup.rows[0].buttons[1].data
                            )
                        )
                        sleep(4)
                        mess = client.get_messages(channel_entity.username)[0]
                        if mess.message == 'Sorry, that task is no longer valid. 😟\n\nUse /join to get a new one.':
                            if a == 2:
                                print(f"{bold}Sorry, that task is no longer valid.{reset}")
                                break
                            client.send_message(channel_entity.username, "/join")
                            a += 1
                        elif mess.message.split("\n")[0] == "Success! 👍":
                            post = mess.message.split('\n')[1:]
                            print(
                                f"{y}[{g}✓{y}] {post}{reset}")
                        else:
                            post = '\n'.join((client.get_messages(channel_entity.username, limit=2)[1].message.split('\n')[1:]))
                            print(
                                f"{y}[{g}✓{y}] {post}{reset}")
                            #ChannelMember(name_chat, int(post[1].split()[-6]))
            except ConnectionError:
                continue

def ChannelMember(channel, hour):
    t = datetime.datetime.now()
    with open("JoinMember.txt", 'a') as f:
        f.write(
            f"{channel} {(t + datetime.timedelta(hours=hour)).strftime('%X')}, ")

def makeclient():
    client = TelegramClient("session/" + phone, api_id, api_hash)
    client.connect()
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            me = client.sign_in(phone, input('Enter your code - '))

        except PhoneCodeInvalidError:
            print("Wrong code, Please try again.")
            sleep(1)
            me = client.sign_in(phone, input('Enter your code - '))
    return client

di = os.listdir("session/")
if di == []:
    phone = input("Enter your number - ")
else:
    phone = di[-1].split('.')[0]
api_id = 4568374
api_hash = "409e0cb48ac927663c164d064079667e"

user = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; CPH1931) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.155 Mobile Safari/537.36"
    }


client = makeclient()

myself = client.get_me()

os.system("cls")

#Banner
print(f"\n{b}TAE{reset}\n")
print('-------------------------------------------')
print(f"{bold}Welcome to Tele-Bot {myself.first_name}!, You can choose the functions below!")
a = menu()

if a == '1':
    dic = {
        '1': "Litecoin_click_bot",
        '2': "BitcoinClick_bot",
        '3': "Dogecoin_click_bot",
        '4': "BTH_clickbot"
    }
    print("\n\n1) LTC\n2) BTC\n3) Doge\n4) BTH\n")
    a = input("Select the Crypto coins - ")
    while (a not in '1234'
           or len(a) >= 2):
        print(f"{r}{bold}{underline}! Invalid input, Please try again.{reset}")
        print("\n\n1) LTC\n2) BTC\n3) Doge\n4) BTH\n")
        a = input("Select the Crypto coins - ")
    channel_entity = client.get_entity(dic[a])
    print()
    sleep(1)
    if len(os.listdir("session/")) != 1:
        numbers = os.listdir("session/")
        n = ''
        for i in range(len(numbers)-1):
            print(f"[{i+1}] {numbers[i].split('.')[0]}", end="  ")
            n += str(i+1)
        print("  [0] or all")
        index = input("Choose your number above or all - ")
        while len(index) != 1 or index not in '0'+n:
            print(f"{r}{bold}{underline}! Invalid input, Please try again.{reset}")
        index = int(index) - 1
        if index == 0:
            for number in numbers:
                phone = number
                client.disconnect()
                client = makeclient()
                myself = client.get_me()
                print(
                    f"\n\nYour accout name: {myself.first_name} {myself.last_name}  Your number:  +{myself.phone}")
                try:
                    client.get_messages(channel_entity)[0]
                except:
                    client.send_message(channel_entity.username, "/start")
                check_InOrderIoUseThisBot()
                print(f"{bold}=========================={reset}")
                print(f"        {B_r}Vist Site{reset}")
                print(f"{bold}=========================={reset}")
                vist_site()
                print(f"\n\n{bold}=========================={reset}")
                print(f"        {B_r}Message Bot{reset}")
                print(f"{bold}=========================={reset}")
                message_bot()
                print(f"\n\n{bold}=========================={reset}")
                print(f"        {B_r}Join Chats{reset}")
                print(f"{bold}=========================={reset}")
                join_chats()
                print('\n'*3)
        else:
            phone = numbers[index].split('.')[0]
            client.disconnect()
            client = makeclient()
            myself = client.get_me()
    print(
        f"\n\nYour accout name: {myself.first_name} {myself.last_name}  Your number:  +{myself.phone}")
    try:
        client.get_messages(channel_entity)[0]
    except:
        client.send_message(channel_entity.username, "/start")
    check_InOrderIoUseThisBot()
    print(f"{bold}=========================={reset}")
    print(f"        {B_r}Vist Site{reset}")
    print(f"{bold}=========================={reset}")
    vist_site()
    print(f"\n\n{bold}=========================={reset}")
    print(f"        {B_r}Message Bot{reset}")
    print(f"{bold}=========================={reset}")
    message_bot()
    print(f"\n\n{bold}=========================={reset}")
    print(f"        {B_r}Join Chats{reset}")
    print(f"{bold}=========================={reset}")
    join_chats()
    print('\n'*3)
    menu()

elif a == '2':
    groups = []
    amount = 0
    print(f"\n\n{bold}=========================={reset}")
    print(f"        {B_b}Leave Channel{reset}")
    print(f"{bold}=========================={reset}")
    sleep(1)
    for ch in client.get_dialogs():
        try:
            print(f"{bold}{ch.name}  {g}Leave Success{reset}")
            client(LeaveChannelRequest(ch.id))
        except:
            continue
        amount += 1

    print(f"\n{y}[{g}✓{y}] Leave Successfully!{reset}")
    print(f"{bold}{underline}Amount Channel: {amount}{reset}")
    print('------------------------------------------\n\n\n')
    menu()

elif a == '3':
    print(f"\n{g}Please enter the number in the format that you use to sign up for Telegram. For example +6661783xxxx{reset}")
    phone = input(f"{bold}Enter your number (To exit this function, type exit.) - {reset}")
    while phone+'.session' in os.listdir("session/"):
        print(f"{r}{underline}! This number already exists{reset}")
        phone = input(f"{bold}Enter your number (To exit this function, type exit.) - {reset}")
    else:
        client = TelegramClient("session/" + phone, api_id, api_hash)
        client.connect()
        client.send_code_request(phone)
        try:
            me = client.sign_in(phone, input(f'{bold}Enter your code - {reset}'))
        except PhoneCodeInvalidError:
            print(f"{r}{bold}{underline}! Wrong code, Please try again.{reset}")
            sleep(1)
            me = client.sign_in(phone, input(f'{bold}Enter your code - {reset}'))
        menu()
