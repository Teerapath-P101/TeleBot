from telethon import TelegramClient, sync
from telethon.tl.functions.channels import *
from telethon.tl.functions.contacts import GetContactsRequest
from telethon.tl.functions.messages import  GetBotCallbackAnswerRequest
from telethon.errors import FloodWaitError, PhoneCodeInvalidError, BotResponseTimeoutError, ChannelsTooMuchError
from telethon.errors.rpcerrorlist import UsernameNotOccupiedError, UsersTooMuchError, UsernameInvalidError
from time import sleep
import os, sys, requests, datetime, re
from requests.exceptions import ConnectionError
from telethon.tl.types import ChannelAdminLogEventActionChangeLocation

if not os.path.exists("session"):
    os.makedirs("session")
s = requests.Session()

#phone = input("ใส่เบอร์โทรศัพท์ - ")
#phone = '+66617837230'
phone = '+66944389353'
api_id = 4568374
api_hash = "409e0cb48ac927663c164d064079667e"
client = TelegramClient("session/" + phone, api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    try:
        me = client.sign_in(phone, input('Enter your code - '))

    except PhoneCodeInvalidError:
        print("Wrong code, Please try again.")
        sleep(2)
        me = client.sign_in(phone, input('Enter your code - '))

user = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; CPH1931) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.155 Mobile Safari/537.36"
    }
myself = client.get_me()

os.system("clear")

#Banner
reset = '\u001b[0m'
r = '\u001b[31;1m'
g = '\u001b[32;1m'
y = '\u001b[38;5;220m'
w = '\u001b[37;1m'

print("TAE")
print(
    f"Welcome to Bot Crypto!!{myself.first_name} {myself.last_name} !!\n")
print("You can choose the functions :")
print("1) Start Bot")
print("2) Leave Channel")
print("3) Add number")

#Functions
def check_InOrderIoUseThisBot():
    mess = client.get_messages(channel_entity)
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

def skipBrowser():
    pass

def wait(sec):
    for i in range(sec, 0, -1):
        print("\r", end="")
        print(f"Please wait {i} seconds to receive the coin", end="")
        sleep(1)
    print('\r',end='')

def skipTask(_data, _id):
    client(
        GetBotCallbackAnswerRequest(
            peer= channel_entity,
            msg_id= _id,
            data= _data
        )
    )

def vist_site():
    client.send_message(channel_entity, "🖥 Visit sites")
    sleep(1)
    mess = client.get_messages(channel_entity)[0]

    if mess.message == "🖥 Visit sites":
        client.send_message(channel_entity, "🖥 Visit sites")
        print("! Server Bot is low")
        while mess == "🖥 Visit sites":
            mess = client.get_messages(channel_entity)[0]

    for _ in range(50):
        sleep(1)
        mess = client.get_messages(channel_entity)[0]
        try:
            if mess.message.split("\n\n")[0] == "Sorry, there are no new ads available. 😟":
                print("Sorry, there are no new ads available")
                break
            else:
                _id = mess.id
                try:
                    url = mess.reply_markup.rows[0].buttons[0].url.strip().strip("'").strip('"')
                except:
                    mess = client.get_messages(channel_entity)[0]
                    url = mess.reply_markup.rows[0].buttons[0].url.strip().strip("'").strip('"')
                res = s.get(
                    url,
                    headers=user,
                    timeout=10,
                    allow_redirects=True
                ).text
                if '  <title>Just a moment...</title>' in res.split('\n'):
                    print(
                        "Skip Checking your browser before accessing")
                    skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                elif 'class="g-recaptcha"' in res.split(' '):
                    print("Skip! This Website has Captcha!")
                    skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                elif 'class="container-fluid"' in res.split(' '):
                    data = re.findall(
                        'class="container-fluid" (.*) data-curr=', res)[0].split()
                    #print(data)
                    timer = data[1].split('=')[1].strip('"')
                    code = data[0].split('=')[1].strip('"')
                    token = data[2].split('=')[1].strip('"')
                    #print(timer, code, token)

                    wait(int(timer))
                    r = s.post("https://dogeclick.com/reward",
                                data={"code": code, "token": token}, headers=user).json()
                    print(
                        f"[✓] {post}")
                else:
                    post = client.get_messages(channel_entity)
                    wait(int(post[0].message.split()[-2]))
                    sleep(1)
                    post = client.get_messages(channel_entity, limit=2)[1].message
                    print(
                        f"[✓] {post}")
        except ConnectionError:
            continue

def join_chats():
    client.send_message(channel_entity, "📣 Join chats")
    a = 0
    sleep(1)
    mess = client.get_messages(channel_entity)[0]

    if mess.message == "📣 Join chats":
        client.send_message(channel_entity, "📣 Join chats")
        print("! Server Bot is low")
        while mess == "📣 Join chats":
            mess = client.get_messages(channel_entity)[0]

    for _ in range(50):
            sleep(1)
            mess = client.get_messages(channel_entity)[0]
            _id = mess.id
            try:
                if mess.message == 'Sorry, that task is no longer valid. 😟\n\nUse/join to get a new one.':
                    if a == 2:
                        print("[\u001b[38;5;1m!] " +
                            "Sorry, that task is no longer valid."+"")
                        break
                    client.send_message(channel_entity, "/join")
                    a += 1
                else:
                    url = mess.reply_markup.rows[0].buttons[0].url
                    res = s.get(
                        url,
                        headers=user,
                        timeout=10,
                        allow_redirects=True
                    ).text
                    if '  <title>Just a moment...</title>' in res.split('\n'):
                        print(
                            "Skip Checking your browser before accessing")
                        skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                    else:
                        name_chat = re.findall(r'<title>Telegram: Contact (.*)</title>', res)[0]
                        try:
                            chat_entity = client.get_entity(name_chat)
                        except:
                            print(
                                "Skip! There is no Telegram account with this username.")
                            skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                            continue
                        try:
                            client(JoinChannelRequest(chat_entity))
                        except UsersTooMuchError:
                            print("Skip! This group is full.")
                            skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                            continue
                        except BotResponseTimeoutError:
                            print("Skip! Servers of this group are low.")
                            skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                        except FloodWaitError:
                            print(
                                "A wait of 207 seconds is required (caused by JoinChannelRequest)")
                            wait(int(210))
                            continue
                        except ChannelsTooMuchError:
                            print("ChannelsTooMuchError")
                            break

                        except:
                            print(
                                "Join Error!\nYou are a member of too many channel! Please use function 'Leave Channel'")
                            break

                        client(
                            GetBotCallbackAnswerRequest(
                                peer=channel_entity,
                                msg_id=_id,
                                data=mess.reply_markup.rows[0].buttons[1].data
                            )
                        )
                        sleep(1)
                        mess = client.get_messages(channel_entity)[0]
                        if mess.message == 'Sorry, that task is no longer valid. 😟\n\nUse /join to get a new one.':
                            if a == 2:
                                print("[\u001b[38;5;1m!] " +
                                    "Sorry, that task is no longer valid."+"")
                                break
                            client.send_message(channel_entity, "/join")
                            a += 1
                        elif mess.message.split("\n")[0] == "Success! 👍":
                            post = '\n'.join((client.get_messages(channel_entity)[0].message.split('\n')[1:]))
                            print(
                                f"[✓] {post}")
                        else:
                            post = '\n'.join((client.get_messages(channel_entity, limit=2)[1].message.split('\n')[1:]))
                            print(
                                f"[✓] {post}")
                            #ChannelMember(name_chat, int(post[1].split()[-6]))
                            #client(LeaveChannelRequest(chat_entity))
            except ConnectionError:
                continue

def message_bot():
    
    client.send_message(channel_entity, "🤖 Message bots")
    sleep(1)
    mess = client.get_messages(channel_entity)[0]
    if mess == "🤖 Message bots":
        client.send_message(channel_entity, "🤖 Message bots")
        print("! Server Bot is low")
        while mess == "🤖 Message bots":
            mess = client.get_messages(channel_entity)[0]
    for _ in range(60):
        try:
            mess = client.get_messages(channel_entity)[0]
            if mess.message.split('\n\n')[0] == 'Sorry, there are no new ads available. 😟':
                print("[\u001b[38;5;1m!] " +
                    "Sorry, there are no new ads available."+"")
                break
            else:
                sleep(1)
                #mess = client.get_messages(channel_entity)[0]
                _id = mess.id
                
                url = mess.reply_markup.rows[0].buttons[0].url
                res = s.get(
                    url,
                    headers=user,
                    timeout=10,
                    allow_redirects=True
                ).text
                if '  <title>Just a moment...</title>' in res.split('\n'):
                    print(
                        "Skip Checking your browser before accessing")
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
                        channel_entity,
                        mess_bot,
                        botChat_entity
                    )
                    sleep(1)
                    post = client.get_messages(channel_entity)[0]
                    if post.message.split('\n\n')[0] == "Sorry, that is not a valid forwarded message.":
                        print(
                            "Skip! This chat bot is not responding.")
                        mess = client.get_messages(channel_entity, limit=3)[2]
                        skipTask(mess.reply_markup.rows[1].buttons[1].data, _id)
                    else:
                        post = client.get_messages(channel_entity, limit=2)[1].message
                        print(
                            f"[✓] {post}")
        except ConnectionError:
            continue

def ChannelMember(channel, hour):
    t = datetime.datetime.now()
    with open("JoinMember.txt", 'a') as f:
        f.write(
            f"{channel} {(t + datetime.timedelta(hours=hour)).strftime('%X')} ")
#a = int(input("Enter your choice - "))
a = 1
if a == 1:
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
        print("! Input Error\nกรุณาเลือกใหม่")
        print("\n\n1) LTC\n2) BTC\n3) Doge\n4) BTH\n")
        a = input("Select the Crypto coins - ")

    channel_entity = client.get_entity(dic[a])
    try:
        client.get_messages(channel_entity)[0]
    except:
        client.send_message(channel_entity, "/start")
    check_InOrderIoUseThisBot()
    vist_site()
    message_bot()
    join_chats()
    #print(mess)
    client.disconnect()

elif a == 2:
    pass
