from urllib import parse

from bs4 import BeautifulSoup

import Requester


def getUrls(search_string , tor,port):
    temp= []
    url = 'https://www.google.com/search?q='
    r = Requester.RequestUrl(port, search_string, tor, url)
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
    except:
        return
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


