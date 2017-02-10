import os

import GoogleDorkSearch
import UrlCheckSqli


def main():
       port="0"

       print("-------------------------------------------------------------------------------------------------------------")
       print("[+] script by pentest30, email : adgroupe@hotmail.com")
       print("[+] The aim of this script is to help you do a quick check for the websites returned from a search based on a list of dorks of you choice if they are vulnerable to SQL injections. ")
       print("[+] at the moment the script can check just for basic sqli weaknesses ......")
       print("-------------------------------------------------------------------------------------------------------------")
       print("the menu: ")
       print ("[+] Please enter the dir of dorks:")
       dir = input()
       if (dir==''):return
       print ("[+] if you wish to use Tor proxy please type yes, if not type no:")
       response = input()
       if (response=='yes'):
           print("[+] would you specify the tor's port please:")
           port = input()
       if (os.path.exists(dir)):
           f = open(dir,"r")
           dorks= f.readlines()
           for d in dorks:
                print ("[+] search for :"+d.strip())
                print('---------------------------------')
                links=GoogleDorkSearch.getUrls(d.strip(), 50)
                if len(links)>0:
                    for l in links:
                        print('---------------------------------')
                        print('[+]  Check if ' + l + " is affected by SQLi")
                        UrlCheckSqli.checkForSqli(l, response, port )



       else:
           print ("file not found!!")

if (__name__ == '__main__'):
    main()
