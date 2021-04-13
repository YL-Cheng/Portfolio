import os
import csv
import time
import tqdm
import random
import requests
import lxml.html
import urllib.request

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar


url = 'https://forums.hardwarezone.com.sg/'
header = {'User-Agent':'Mozilla/5.0'}
requ = urllib.request.Request(url,headers=header)
data = urllib.request.urlopen(requ).read()
forums_m = lxml.html.fromstring(data.decode('cp1252'))

sub_forums = []
for sublink in forums_m.xpath('//*[@class="alt1Active"]/div[1]/a'):
    print(sublink.attrib.get('href'))
    sub_forums.append(sublink.attrib.get('href'))
    time.sleep(random.randint(1,3))
    
with open('sub_forums.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['sub_forums_url'])
    for p in sub_forums:
        writer.writerow([p])