from telethon import TelegramClient, client, sync
from telethon.sessions import StringSession
from telethon.tl.functions.channels import JoinChannelRequest, LeaveChannelRequest
from time import sleep
import os, datetime, json

bot_username = {
    '1': "Litecoin_click_bot",
    '2': "BitcoinClick_bot",
    '3': "Dogecoin_click_bot",
    '4': "BCH_clickbot",
    '5': 'Zcash_click_bot'
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

if not os.path.exists(".phone_session.json"):
    with open('.phone_session.json', 'w') as w:
        w.write('{}')
phone_session = json.load(open('.phone_session.json', 'r'))

def menu():
    print(f"{bold}\nYour accout name: {b}{me.first_name} {me.last_name}{reset} Your number: {b}+{me.phone}{reset}")
    print(f"{bold}1) Start bot")
    print("2) Leave channel")
    print("3) Add account")
    print("4) Delete account")
    print("5) Check account")
    print(f"6) Quit{reset}")
    f = input("Enter your choice - ")
    while not main_menu.get(f):
        print(f"{r}{underline}Input invalid!{reset} Please enter again.")
        f = input("Enter your choice - ")
    return f, True
def create_acc(new_client=False):
    global phone_session
    if new_client:
        client = TelegramClient(StringSession(), api_id, api_hash)
        client.start()
        number = (client.get_me()).phone
        phone_session[number] = client.session.save()
        with open('.phone_session.json', 'w') as w:
            json.dump(phone_session, w)
    else:
        client = TelegramClient(StringSession(str_sess), api_id, api_hash)
        client.start()
    return client

def waitforcoin(sec):
    for i in range(sec, 0, -1):
        print("\r", end="")
        print(f"{bold}Please wait {i} seconds to receive  ", end="")
        sleep(1)
    print(f'{reset}\r', end='')

def Start():
    pass
def leave():
    print(f"\n\n{bold}=========================={reset}")
    print(f"      {B_b}Leave Channel{reset}")
    print(f"{bold}=========================={reset}\n")
    for i, cli in enumerate(clients):
        amount = 0
        me = cli.get_me()
        print(f"{bold}It will run all accounts! "+ (f"(There are {len(clients)}.)" if len(clients)>1 else f"(There is 1.)")+ reset)
        print(f"\n{bold}{i+1}. {cyan}{me.first_name} {me.last_name} ({cyan}+{me.phone}){reset}")
        for dialog in client.iter_dialogs():
            try:
                print(f"    {bold}{dialog.entity.title}  {g}Leave Success{reset}")
                client(LeaveChannelRequest(dialog))
                amount += 1
            except:
                continue
        print(f"{bold}Account: {cyan}{me.first_name} {me.last_name} ({cyan}+{me.phone}) ")
        print(f"\n{y}[{g}✓{y}] Leave Successfully!{reset}")
        print(f"{bold}{underline}Total Channel: {amount}{reset}")
        print('\n------------------------------------------\n\n')
def add():
    global clients
    print(f"{cyan}To exit, press Ctrl+C+Enter{reset}")
    try:
        clients.append(create_acc(new_client=True))
        print(f"{g}Account added Successfully!{reset}")
    except KeyboardInterrupt:
        pass
def delete():
    global phone_session
    if len(clients)==1:
        print("You have 1 account only! You can not delete it.")
    else:
        phone_keys = list(phone_session)
        try:
            for i, cli in enumerate(clients):
                me = cli.get_me()
                print(
                    f"{i+1}) {cyan}{me.first_name} {me.last_name} {reset}({cyan}+{me.phone}{reset})")
            k = int(input(f"{bold}Enter your choice to delete (To exit, press Ctrl+C+Enter) - "))-1
            while not phone_session.get(phone_keys[k]):
                print(f"{r}Invaild! Please try again{reset}")
                k = int(input(f"{bold}Enter your choice to delete (To exit, press Ctrl+C+Enter) - "))-1
            clients[k].disconnect()
            del phone_session[phone_keys[k]], clients[k]
            with open('.phone_session.json', 'w') as w:
                w.write(phone_session)
            print(f"{g}{bold}The account has been deleted!{reset}")
        except KeyboardInterrupt:
            pass
def check():
    print("There are "+len(clients)+" account" if len(clients)>1 else "There is 1 account")
    for i, client in enumerate(clients):
        me = client.get_me()
        print(f"    {i+1}. {me.first_name} {me.last_name} (+{me.phone})")
def Quit():
    for client in clients:
        client.disconnect()
    print(f"{g}{bold}Bye, See you again Thanks for using this bot :){reset}")
    exit()

api_id = 5330210
api_hash = "a112ebb70ccee839801ef08744372fff"
try:
    if phone_session == {}:
        clients = []
        client = create_acc(new_client=True)
        clients.append(client)
    else:
        clients = []
        for phone in phone_session:
            str_sess = phone_session[phone]
            clients.append(create_acc())
        client = clients[0]
    me = client.get_me()
    os.system('cls' if os.name == 'nt' else 'clear')
    main_menu = {"1": Start, "2": leave, "3": add,
                "4": delete, "5": check, "6": Quit}
    banner = f"""
{bold}{r}████████╗ █████╗ ███████╗     
{reset}╚══██╔══╝██╔══██╗██╔════╝         
   {b}██║   ███████║█████╗ {reset}          
   ██║   ██╔══██║██╔══╝           
   {r}██║   ██║  ██║███████╗██╗██╗██╗
   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝╚═╝╚═╝{reset}
                                    """
    print(banner)
    print(me)
    m = menu()
    while m[1]:
        print("\n")
        main_menu[m[0]]()
        m = menu()

finally:
    for client in clients:
        client.disconnect()
