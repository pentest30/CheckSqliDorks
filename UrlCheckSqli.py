import os
import random
import sys
import threading
import time
from urllib.parse import urlparse, parse_qs

import requests
from bs4 import BeautifulSoup
from colorama import *
from requests.packages.urllib3.exceptions import InsecureRequestWarning

import Result

results = []


def saveResults(payload, url):
    r1 = Result.Result(url, payload, "MySQl server", "")
    for rrr in results:
        if rrr.url == r1.url:
            # threading.Lock().release()
            return
    results.append(r1)
    dir = os.getcwd() + "/result.csv"
    writer = open(dir, 'a')
    writer.write('\n' + "Url: " + r1.url )
    writer.close()


def preparePOSTRequest(port, toruse, url ,data):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    dir = os.getcwd() + "/user-agents/user-agents.txt"
    f = open(dir, "r")
    headers = f.readlines()
    rd = random.randint(0, len(headers) - 1)
    header = {"user-agent": headers[rd].strip()}
    try:


        if toruse == "yes":
            proxies = {'socks5': '127.0.0.1:' + port}
            r = requests.get(url, headers=header,params=data, proxies=proxies, verify=False)
        else:
            r = requests.get(url, headers=header,params=data,  verify=False)

        return r
    except:
        return


def blindSqlCHeck():
    pass


def runSqliTest(url, payload, toruse, port , fuzzingType):

    for rrr in results:
        if url == rrr.url:
            #threading.Lock().release()
            return

    o = urlparse(url)
    query = parse_qs(o.query)

    # check if the methode is a GET or POST
    if query != {}:
        data = {}
        for q in query:
            data[q] = payload

        r = preparePOSTRequest(port, toruse,o.geturl() , data)
        if (fuzzingType =="Normal"):basicSqliCheck(r,url, payload)
        else:blindSqlCHeck()
    elif query=={}:
        r = preparePOSTRequest(port, toruse, url ,{})
        if r!='':
           try:
               soup = BeautifulSoup(r.text, 'html.parser')
               forms = soup.findAll('input', value=True)
               data = {}
               if len(forms) > 0:
                   for f in forms:
                       data.update( f["name"], payload)
                   r2 = preparePOSTRequest(port, toruse, url ,data)
                   basicSqliCheck(r2, url, payload)

           except:
               return


def basicSqliCheck(r,url, payload):
    if r == '':
        return

    else:
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            text = ''.join(soup.text)
            if (
                            'Microsoft OLE DB Provider for ODBC Drivers error' in text or 'Microsoft SQL Native Client error' in text):
                print(Fore.RED,Style.BRIGHT, "[+] seems to be vulnerable to SQL injection")
                print(Fore.GREEN,Style.BRIGHT," [+] Possible database : MS SQl server")
                saveResults(payload, url)
                return

            elif ("error in your SQL syntax" in text):
                print(Fore.RED,Style.BRIGHT,"[+] seems to be vulnerable to SQL injection")
                print(Fore.GREEN,Style.BRIGHT,"[+] Possible database: MySQl")
                saveResults(payload, url)
                return

            elif ("SQL command not properly ended" in text):
                print(Fore.RED,Style.BRIGHT,"[+] seems to be vulnerable to SQL injection")
                print(Fore.GREEN,Style.BRIGHT,"[+] Possible database :Oracle")
                saveResults(payload, url)
                return
            elif ("Query failed: ERROR: syntax error at or near" in text):
                print(Fore.RED,Style.BRIGHT,"[+] seems to be vulnerable to SQL injection")
                print(Fore.GREEN,Style.BRIGHT,"[+] Possible database :Oracle")
                saveResults(payload, url)
                return


        except BaseException as e:
            #print(str(e))
            return



def prepareGetRequest(port, toruse, url):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    dir = os.getcwd() + "/user-agents/user-agents.txt"
    f = open(dir, "r")
    headers = f.readlines()
    rd = random.randint(0, len(headers) - 1)
    header = {"user-agent": headers[rd].strip()}
    try:

        if toruse == "yes":
            proxies = {'socks5': '127.0.0.1:' + port}
            r = requests.get(url, headers=header, proxies=proxies, verify=False)
        else:
            r = requests.get(url, headers=header, verify=False)

        return r
    except:
        return


def checkForSqli(url, torUse, port):
    threads = []
    dir = os.getcwd() + "/payloads/"
    for subdir, dirs, files in os.walk(dir):
        for f in files:
            fi = open(dir + "/" + f, "r")
            paylaods = fi.readlines()
            for p in paylaods:
                if f.find('blind') > -1:
                    tt =random.randint(3,20)
                    p.replace('__TIME__', str(tt))
                    fuzzing="Blind"
                else:fuzzing="Normal"

                t = threading.Thread(target=runSqliTest, args=(url, p, torUse, port,fuzzing,))
                threads.append(t)
                try:
                   try:
                       t.start()
                       time.sleep(0.1)
                   except:time.sleep(0.2)
                except (KeyboardInterrupt, SystemExit) :

                    print (Fore.RED," [-] Ctrl-c received! Sending kill to threads...")
                    for t in threads:
                        t.kill_received = True
                    sys.exit()






def displayResults():
    if (len(results) > 0):
        print('[+] Number of affected websites is:' + str(len(results)))
        for rr in results:
            print(Fore.GREEN,Style.BRIGHT,
                "[+] " + "Url: " + rr.url + " [+] payload: " + rr.payload + "[+] database : " + rr.dataType)
