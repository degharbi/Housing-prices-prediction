from bs4 import BeautifulSoup
import requests
from time import sleep
from random_headers import LoadHeader
import html5lib

def htmltext(url, proxy):
    try:
        r = requests.get(url, headers=LoadHeader(), proxies=proxy, timeout=2)
        htmltext = r.text
        return htmltext
    except: print("can't get page : "+str(r))

def requests_soup(url, headers, proxy, timeout):
    try:
        soup = BeautifulSoup(requests.get(url, headers=headers, proxies=proxy, timeout=timeout).content, "html.parser")
        return(soup)
    except:
        pass 
        # return print("Make_soup : Couldn't get soup with requests")

def selenium_soup(url, proxy):
    options=webdriver.ChromeOptions()
    # options.add_argument('headless')
    # desired_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    # desired_capabilities['proxy'] = {
    #     "httpProxy":proxy,
    #     "ftpProxy":None,
    #     "sslProxy":None,
    #     "noProxy":None,
    #     "proxyType":"MANUAL",
    #     "class":"org.openqa.selenium.Proxy",
    #     "autodetect":False
    # }

    try:
        # browser = webdriver.Remote("http://localhost:4444/wd/hub", desired_capabilities)
        browser = webdriver.Chrome('c:/users/djamel/desktop/zigzagimmo/chromedriver.exe', chrome_options=options)  
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, html5lib)
        browser.close()
        return soup 
    except:
        return print("Couldn't access sourcecode")
