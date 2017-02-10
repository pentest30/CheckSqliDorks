import os
import random

import requests
from bs4 import BeautifulSoup


def getUrls(search_string, start):
    temp= []
    url='https://bing.com/search'
    payload= { 'q' : search_string, 'start' : start }
    dir=os.getcwd()+"/user-agents/user-agents.txt"
    f = open(dir, "r")
    headerslist = f.readlines()
    r=random.randint(0, len(headerslist))
    header ={"user-agent" : headerslist[r].strip()}
    session = requests.Session()
    session.trust_env = False
    r= session.get( url, params = payload , headers=header)

    soup= BeautifulSoup( r.text, 'html.parser' )
    h3tags= soup.find_all( 'h2' )
    #print(h3tags)
    if (len(h3tags)>0):
        for h3 in h3tags:
            try:
                temp.append(h3.find('a').get('href'))

            except:
                #print("[-] there is a problem")
                continue

    return temp