import csv
import os
import random
import threading
import time
import requests
import Result
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning

results = []
def runSqliTest (url,payload, toruse, port):
    for rrr in results:
        if (rrr.url == url) :return

    r = prepareRequest(port, toruse, url+payload)
    if (r==''):return

    else:
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            text = ''.join(soup.text)
            if('Microsoft OLE DB Provider for ODBC Drivers error' in text or 'Microsoft SQL Native Client error' in text ):
                print("[+] seems to be vulnerable to SQL injection")
                print(" [+] Possible database system manager: MS SQl server")
                r1= Result(url, payload, "MS SQl server","")
                results.append(r1)

            elif ("error in your SQL syntax" in text ):
                print("[+] seems to be vulnerable to SQL injection")
                print ("Possible database system manager: MySQl")
                saveResults(payload, url)

            elif ( "SQL command not properly ended"in text ):
                print("[+] seems to be vulnerable to SQL injection")
                print("Possible database system manager :Oracle")
                saveResults(payload, url)
            elif ("Query failed: ERROR: syntax error at or near" in text):
                print("[+] seems to be vulnerable to SQL injection")
                print("Possible database system manager :Oracle")
                saveResults(payload, url)


        except :return
    return


def saveResults(payload, url):
    r1 = Result(url, payload, "MySQl server", "")
    results.append(r1)
    dir = os.getcwd()
    writer = csv.writer(open(dir + "/results", 'w'))
    writer.writerows(r1)


def prepareRequest(port, toruse, url):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    dir = os.getcwd() + "/user-agents/user-agents.txt"
    f = open(dir, "r")
    headerslist = f.readlines()
    rd = random.randint(0, len(headerslist)-1)
    header = {"user-agent": headerslist[rd].strip()}
    try:
        if (toruse == "yes"):
            proxies = {'socks5': '127.0.0.1:' + port}
            r = requests.get(url, headers=header, proxies=proxies, verify=False)
        else:
            r = requests.get(url, headers=header, verify=False)
        return r
    except:return


def checkForSqli(url, torUse, port):
    threads = []
    dir = os.getcwd() +"/paylaods/"
    for subdir, dirs, files in os.walk(dir):
        for f in files:
            fi = open(dir +"/" +f , "r")
            paylaods = fi.readlines()
            for p in paylaods:
                pp =url+p
                #runSqliTest(url, torUse, port)
                t = threading.Thread(target=runSqliTest, args=(url,p,torUse,port,))
                threads.append(t)
                t.start()
            time.sleep(5)

    if (len(results)>0):
        print('[+] Number of affected websites is:' + str(len(results)))
        dir = os.getcwd()
        writer = csv.writer(open(dir+"/results", 'w'))
        for rr in results:
            print("[+] " + "Url:" + rr.url + " oaylaod:" + rr.paylaod + " database system manager:" + rr.datatype)
            writer.writerows(rr)







