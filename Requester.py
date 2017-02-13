import datetime
import os
import random

import requests


def RequestUrl(port, search_string, tor, url):
    t ="["+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+ str(datetime.datetime.now().second)
    dir = os.getcwd() + "/user-agents/user-agents.txt"
    f = open(dir, "r")
    headerslist = f.readlines()
    rd = random.randint(0, len(headerslist) - 1)
    header = {"user-agent": headerslist[rd].strip()}
    try:
        if tor == "yes":
            proxies = {'socks5': '127.0.0.1:' + port}
            r = requests.get(url + search_string, headers=header, proxies=proxies)
        else:
            r = requests.get(url + search_string, headers=header)
        return r
    except requests.ConnectionError:
        print(t+ "]  connexion errors !!" )