import datetime
import os

from colorama import *

import GoogleDorkSearch
import UrlCheckSqli
import MiniCrawler

def main():

       port="0"
       print(Fore.GREEN,' $$$$$$\  $$\                           $$\        $$$$$$\            $$\ $$\ $$$$$$$\                      $$\                 ')
       print(Fore.GREEN,'$  __$$\ $$ |                          $$ |      $$  __$$\           $$ |\__|$$  __$$\                     $$ |                ')
       print(Fore.GREEN,'$$ /  \__|$$$$$$$\   $$$$$$\   $$$$$$$\ $$ |  $$\ $$ /  \__| $$$$$$\  $$ |$$\ $$ |  $$ | $$$$$$\   $$$$$$\  $$ |  $$\  $$$$$$$\ ')
       print(Fore.GREEN,'$$ |      $$  __$$\ $$  __$$\ $$  _____|$$ | $$  |\$$$$$$\  $$  __$$\ $$ |$$ |$$ |  $$ |$$  __$$\ $$  __$$\ $$ | $$  |$$  _____|')
       print(Fore.GREEN,'$$ |      $$ |  $$ |$$$$$$$$ |$$ /      $$$$$$  /  \____$$\ $$ /  $$ |$$ |$$ |$$ |  $$ |$$ /  $$ |$$ |  \__|$$$$$$  / \$$$$$$\ ')
       print(Fore.GREEN,'$$ |  $$\ $$ |  $$ |$$   ____|$$ |      $$  _$$<  $$\   $$ |$$ |  $$ |$$ |$$ |$$ |  $$ |$$ |  $$ |$$ |      $$  _$$<   \____$$\ ')
       print(Fore.GREEN,'\$$$$$$  |$$ |  $$ |\$$$$$$$\ \$$$$$$$\ $$ | \$$\ \$$$$$$  |\$$$$$$$ |$$ |$$ |$$$$$$$  |\$$$$$$  |$$ |      $$ | \$$\ $$$$$$$  |')
       print(Fore.GREEN,' \______/ \__|  \__| \_______| \_______|\__|  \__| \______/  \____$$ |\__|\__|\_______/  \______/ \__|      \__|  \__|\_______/ ')
       print(Fore.GREEN,'                                                                  $$ |                                                          ')
       print(Fore.GREEN,'                                                                  $$ |                                                          ')
       print(Fore.GREEN,"                                                                  \__|                                                          ")
       print( "THE MENU: ")
       print(Fore.YELLOW, Style.BRIGHT, "1) -search by dorks:")
       print(Fore.YELLOW, Style.BRIGHT, "2) -scan a given URL:")
       choice = input("# ")
       print(choice)
       if choice=="1":
           print (Fore.YELLOW,"[+] Please enter the dir of dorks:")
           dir = input()
           if (dir==''):return
           print (Fore.YELLOW,Style.BRIGHT,"[+] if you wish to use Tor proxy please type yes, if not type no:")
           response = input()
           if (response=='yes'):
               print(Fore.YELLOW,Style.BRIGHT,"[+] would you specify the tor's port please:")
               port = input()
           if (os.path.exists(dir)):
               f = open(dir,"r")
               dorks= f.readlines()
               for d in dorks:
                    if d=='':continue
                    print (Fore.RED,Style.BRIGHT,"["+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+ str(datetime.datetime.now().second)+ "] search for :"+d.strip())
                    links=GoogleDorkSearch.getUrls(d.strip() , response, port)
                    if len(links)>0:
                        for l in links:
                            print('---------------------------------')
                            print(Fore.WHITE,Style.BRIGHT,"["+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+ str(datetime.datetime.now().second)+ ']  Current URL ' + l  )
                            UrlCheckSqli.checkForSqli(l, response, port )
                    else:continue



           else:
               print (Style.BRIGHT,"[-] file not found!!")
       else:
           print(Fore.YELLOW, "[+] Please enter the URL:")
           url = input("# ")
           MiniCrawler.crawl(url,'')
if (__name__ == '__main__'):
    main()
