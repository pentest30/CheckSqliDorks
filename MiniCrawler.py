import re
import Requester
result = []
link_re = re.compile(r'href="(.*?)"')

def crawl (url):
    try:



        req = Requester.RequestUrl('9050','','yes',url.strip())
        if (req.status_code!=200):
            return []
        links = link_re.findall(req.text)
        exist = False
        for l in links:
           if (l.find("http")==-1):
               for r in result:
                   if l in r:
                       exist = True
                       break

               if (exist == True):
                    exist = False
                    continue
           else:continue
           if (l.startswith('/')):
               uri = url + l
           else:
               uri=url + "/" + l

           result.append(uri)
           crawl(uri)


        print (result)
    except:return []