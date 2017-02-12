import os
import GoogleDorkSearch
import UrlCheckSqli
import argparse
from colorama import *
def main():
       port="0"


       print(Fore.GREEN,"##############################################################")
       print(Fore.GREEN,"[+] script by pentest30, email : adgroupe@hotmail.com")
       print(Fore.GREEN,"[+] The aim of this script is to help you do a quick check for the websites returned from a search based on a list of dorks of your choice \n "
                        "if they are vulnerable to SQL injections. ")
       print(Fore.GREEN,"[+] at the moment the script can check just for basic sqli weaknesses!")
       print(Fore.GREEN,"#############################################################")
       print( "THE MENU: ")
       print (Fore.YELLOW,"[+] Please enter the dir of dorks:")
       dir = input()
       if (dir==''):return
       print (Fore.YELLOW,"[+] if you wish to use Tor proxy please type yes, if not type no:")
       response = input()
       if (response=='yes'):
           print(Fore.YELLOW,"[+] would you specify the tor's port please:")
           port = input()
       if (os.path.exists(dir)):
           f = open(dir,"r")
           dorks= f.readlines()
           for d in dorks:
                print (Fore.RED,"[+] search for :"+d.strip())
                links=GoogleDorkSearch.getUrls(d.strip() , response, port)
                if len(links)>0:
                    for l in links:
                        print('---------------------------------')
                        print(Fore.BLUE,'[+]  Current URL ' + l  )
                        UrlCheckSqli.checkForSqli(l, response, port )



       else:
           print ("[-] file not found!!")

if (__name__ == '__main__'):
    main()
