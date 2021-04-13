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

proxy_pool = open('proxy_pool.txt').readlines()

def read_pathcsv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        raw = list(reader)
    out_list = [item for sublist in raw[1:] for item in sublist]
    return out_list

def write_pathcsv(filename, col_name, data):
    if '.csv' not in filename:
        filename = filename + '.csv'
    with open(filename, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([col_name])
        for line in data:
            writer.writerow([line])

def use_proxy(proxy_addr, url):
    proxy = urllib.request.ProxyHandler({'http': proxy_addr})
    opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    # data = urllib.request.urlopen(url).read().decode('utf-8')
    data = urllib.request.urlopen(url).read()
    return data

def find_available_ip(url, proxy_pool):
    ip_check = False
    #addr = 0
    #proxy_addr = proxy_pool[addr]
    proxy_addr = proxy_pool[0]
    while not ip_check:
        try:
            data = use_proxy(proxy_addr, url)
            ip_check = True
        except:
            ip_check = False
            del proxy_pool[0]
            proxy_addr = proxy_pool[0]
            #addr+=1
            #proxy_addr = proxy_pool[addr]
    return data, proxy_pool

sub_forums = read_pathcsv('sub_forums.csv')


url = 'https://forums.hardwarezone.com.sg/'
header = {'User-Agent':'Mozilla/5.0'}

post = {}
for sublink in sub_forums[26:-3]:
    post[sublink] = []
    
    pagelink = sublink
    next_page = True
    page = 1
    while next_page and page <= 50:
        print(sublink)
        url_s = url[:-1]+pagelink
        data_s, proxy_pool = find_available_ip(url_s, proxy_pool)
        forums_s = lxml.html.fromstring(data_s.decode('cp1252'))
        try:
            page = forums_s.find('.//li[@class="current"]/a').text
            page = int(page)
            print('#', page)
            print(type(page))
        except:
            print('# 1')
        
        for plink in forums_s.xpath('//a[contains(@id, "thread_title_")]'):
            time.sleep(random.randint(1,3))
            print(plink.attrib.get('href'))
            post[sublink].append(plink.attrib.get('href'))
        time.sleep(10)
        try:
            pagelink = forums_s.xpath('.//a[contains(text(),"Next ›")]')[0].attrib.get('href')
            next_page = True
        except:
            next_page = False
        print('-'*10)
    
        filename = sublink[1:-1].replace('-', '_')+'.csv'
        write_pathcsv('post/'+filename, 'post_link', post[sublink])
    
    filename = sublink[1:-1].replace('-', '_')+'_full.csv'
    write_pathcsv('post/'+filename, 'post_link', post[sublink])