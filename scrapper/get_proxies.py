from bs4 import BeautifulSoup
import requests, json
from threading import Thread
import make_soup

global proxies
proxies = []

def check_proxy(proxy):
    try: 
        r = requests.get('https://httpbin.org/ip', proxies= proxy, timeouts= 1)
        if r.json()['origin'] == proxy['https'].split(':')[0]: return True
        else: return False
    except: return False

def get_soup(site):
    try: 
        soup = BeautifulSoup(requests.get(site, headers={"user-agent": "Mozilla/5.0"}).content, "html.parser")
        if site == "https://free-proxy-list.net/":
            for row in soup.find("tbody").findAll("tr"):
                ip = row.findAll("td")[0].text
                port = row.findAll("td")[1].text
                https = row.findAll("td")[6].text
                add = json.loads(json.dumps({'https' : ip +':'+ port, 'http' : ip +':'+ port}))
                if add not in proxies and https=="yes" and check_proxy(add):
                    proxies.append(add)
        if False and site == 'https://hidemyna.me/en/proxy-list/?type=s#list':
            for row in soup.find(class_="proxy_t").tbody.findAll("tr"):
                print(row)
                ip = row.findAll("td")[0].text
                port = row.findAll("td")[1].text
                https = row.findAll("td")[4].text
                if str({"https": str(ip+':'+port)}) not in proxies and "HTTPS" in https:
                    proxies.append({"https": str(ip+':'+port)})   
                    print(proxies[len(proxies)-1])
        if False and site == "https://www.proxynova.com/proxy-server-list/":
            for row in soup.find('table', {"id":"tbl_proxy_list"}).tbody.findAll("tr"):
                print(row)
                ip = row.findAll("td")[0].text
                port = row.findAll("td")[1].text
                https = row.findAll("td")[4].text
                if str({"https": str(ip+':'+port)}) not in proxies and "HTTPS" in https:
                    proxies.append({"https": str(ip+':'+port)})   
                    print(proxies[len(proxies)-1])
        if site == 'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt':
            r = requests.get('https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt')
            proxylist = r.text.split('\n')
            for row in proxylist[1:len(proxylist)-1]:
                if '-S' in row:# and '+' in row:
                    proxy = row.split(' ')[0]
                    add = json.loads(json.dumps({'https' : proxy, 'http' : proxy}))
                    if add not in proxies: 
                        proxies.append(add)       
    except: pass 

def gather_proxies():
    sites_proxy = [
        'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt',
        "https://free-proxy-list.net/", 
        'https://hidemyna.me/en/proxy-list/?type=s', 
        "http://spys.one/en/https-ssl-proxy/", 
        "https://www.proxynova.com/proxy-server-list/"]

    threadlist = []
    for site in sites_proxy[0:2]:
        t = Thread(target= get_soup, args=(site,))
        t.start()
        threadlist.append(t)

    for b in threadlist:
        b.join()
    # print('Number of proxies: '+str(len(proxies)))
    return(proxies)

