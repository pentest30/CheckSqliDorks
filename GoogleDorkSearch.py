import os
import random
from urllib import parse

import requests
from bs4 import BeautifulSoup


def getUrls(search_string , tor,port):
    temp= []
    url = 'https://www.google.com/search?q='
    dir=os.getcwd()+"/user-agents/user-agents.txt"
    f = open(dir, "r")
    headerslist = f.readlines()
    rd=random.randint(0, len(headerslist)-1)
    header = {"user-agent": headerslist[rd].strip()}

    if tor == "yes":
        proxies = {'socks5': '127.0.0.1:' + port}
        r = requests.get(url + search_string, headers=header, proxies=proxies)
    else:r= requests.get( url + search_string,  headers=header)
    soup= BeautifulSoup( r.text, 'html.parser' )
    h3tags= soup.find_all( 'h3' )

    if (len(h3tags)>0):
        for h3 in h3tags:
            try:
                pos= parse.unquote(h3.find('a').get('href').replace("/url?q=", '')).find("&sa")
                ut = parse.unquote(h3.find('a').get('href').replace("/url?q=", '').replace('&lang=en',''))

                if (ut.find('&lang=en')>-1):ut.replace('&lang=en','')
                if (ut.find('http://www.google.com/url?url=')>-1): ut.replace('http://www.google.com/url?url =', '')
                if (ut.find('&rct=j&q=&esrc=s') > -1): ut.replace('&rct=j&q=&esrc=s', '')


                if (pos>-1):
                    s =0
                    ur =""
                    for ch in ut:
                        if (s<pos):ur =ur+ch
                        else:break
                        s =s +1
                    temp.append(ur)

                else:temp.append(ut)


            except:
                #print("[-] there is a problem")
                continue

    return temp