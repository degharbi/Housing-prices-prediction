import json, sqlite3
from time import time, sleep
from get_proxies import gather_proxies
import random, csv, os, requests

def htmltext(url, proxy, headers):
    try:
        r = requests.get(url, headers=headers, proxies=proxy, timeout=2)
        htmltext = r.text
        return htmltext
    except: print("can't get page : "+str(url))

UserAgentCSV = open('user_agent.csv', 'r')
UserAgentList = csv.reader(UserAgentCSV)
UserAgentList = [row for row in UserAgentList]
UserAgentList = [l[0] for l in UserAgentList]

with open('zips.csv', 'r') as f: zips = [line.replace('\n','') for line in f]

# for zip in zips[1:2]:
zip = zips[3]
lr= {
    "content": "buy_sold",
    "targets": {
        "zip": zip,
        "state": "WA",
        "cnty": "King"
    }
}
url_geo = 'https://www.zillow.com/ads/GetSearchPageAdRequest.htm?lr='+str(lr)

proxies = gather_proxies()
print('nombre de proxy {}'.format(len(proxies)))

random.shuffle(proxies)
proxy = random.choice(proxies)
random.shuffle(UserAgentList)

headers = {'User-Agent': random.choice(UserAgentList).strip()}

htmlgeo = htmltext(url_geo, proxy, headers)
htmlgeo = json.dumps(htmlgeo)
latitude = int(htmlgeo['targets']['mlat']) * 1000000
longitude = int(htmlgeo['targets']['mlong']) * 1000000

q = 'https://www.zillow.com/search/GetResults.htm?&\
status=001000&\
rect='+-(longitude+322037/2)+','+(latitude-167284/2)+','+-(longitude-322037/2)+','+(latitude+167284/2)+'&\
search=maplist'
html = htmltext(q, proxy, headers)        

with open('{}.json'.format(zip), 'w') as f: 
    f.write(html)
