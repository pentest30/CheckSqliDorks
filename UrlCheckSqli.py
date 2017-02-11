import os
import random
import threading
import time
from urllib.parse import urlparse, parse_qs
import requests
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import Result

results = []


def saveResults(payload, url):
    r1 = Result.Result(url, payload, "MySQl server", "")
    results.append(r1)
    dir = os.getcwd() + "/result.txt"
    writer = open(dir, 'a')
    writer.write('\n' + "Url: " + r1.url + " paylaod: " + r1.paylaod + " database system manager: " + r1.dataType)
    writer.close()


def runSqliTest(url, payload, toruse, port):
    o = urlparse(url)
    query = parse_qs(o.query)
    if query != {}:
        r = prepareRequest(port, toruse, url + payload)
        basicGetSqliCheck(r,url, payload)
    elif query=={}:
        print("")



def basicGetSqliCheck(r,url, payload):
    for rrr in results:
        if rrr.url in url or url in rrr.url:
            break
            return


    if r == '':
        return

    else:
        try:
            soup = BeautifulSoup(r.text, 'html.parser')
            text = ''.join(soup.text)
            if (
                            'Microsoft OLE DB Provider for ODBC Drivers error' in text or 'Microsoft SQL Native Client error' in text):
                print("[+] seems to be vulnerable to SQL injection")
                print(" [+] Possible database system manager: MS SQl server")
                saveResults(payload, url)
                return

            elif ("error in your SQL syntax" in text):
                print("[+] seems to be vulnerable to SQL injection")
                print("Possible database system manager: MySQl")
                saveResults(payload, url)
                return

            elif ("SQL command not properly ended" in text):
                print("[+] seems to be vulnerable to SQL injection")
                print("Possible database system manager :Oracle")
                saveResults(payload, url)
                return
            elif ("Query failed: ERROR: syntax error at or near" in text):
                print("[+] seems to be vulnerable to SQL injection")
                print("Possible database system manager :Oracle")
                saveResults(payload, url)
                return


        except BaseException as e:
            print(str(e))
            return


def prepareRequest(port, toruse, url):
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    dir = os.getcwd() + "/user-agents/user-agents.txt"
    f = open(dir, "r")
    headers = f.readlines()
    rd = random.randint(0, len(headers) - 1)
    header = {"user-agent": headers[rd].strip()}
    try:
        # check if the methode is a GET or POST

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
    dir = os.getcwd() + "/paylaods/"
    for subdir, dirs, files in os.walk(dir):
        for f in files:
            fi = open(dir + "/" + f, "r")
            paylaods = fi.readlines()
            for p in paylaods:
                pp = url + p
                # runSqliTest(url, p,torUse, port)
                t = threading.Thread(target=runSqliTest, args=(url, p, torUse, port,))
                threads.append(t)
                t.start()
                time.sleep(0.05)

    try:
        if (len(results) > 0):
            print('[+] Number of affected websites is:' + str(len(results)))
            for rr in results:
                print(
                    "[+] " + "Url: " + rr.url + " paylaod: " + rr.paylaod + " database system manager: " + rr.dataType)
                # writer.writerows(rr)
    except:
        return
