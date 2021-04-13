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
    http_status = int(data.getcode())
    print(http_status)
    return data, http_status

def find_available_ip(url, proxy_pool):
    ip_check = False
    #addr = 0
    #proxy_addr = proxy_pool[addr]
    proxy_addr = proxy_pool[0]
    while not ip_check:
        try:
            data, http_status = use_proxy(proxy_addr, url)
            ip_check = True
        except:
            ip_check = False
            del proxy_pool[0]
            proxy_addr = proxy_pool[0]
            #addr+=1
            #proxy_addr = proxy_pool[addr]
    
    if http_status == 200:
        return data, proxy_pool
    else:
        return None, proxy_pool


url = 'https://forums.hardwarezone.com.sg/'
header = {'User-Agent':'Mozilla/5.0'}

curr_subf = os.listdir( os.path.join( os.getcwd(), 'post') )
curr_subf.remove('.DS_Store')
curr_subf = [f for f in curr_subf if '_full.csv' in f]

drop_subf = os.listdir( os.path.join( os.getcwd(), 'post') )
drop_subf.remove('.DS_Store')
drop_subf = [f for f in drop_subf if '_comments_all.csv' in f]

forums_to_scrap = []
for sub in curr_subf:
    if sub[:-9]+'_comments_all.csv' not in drop_subf:
        forums_to_scrap.append(sub)
    else:
        pass

print('Forums to scrap: \n', forums_to_scrap)

for f in forums_to_scrap:
    forums_s = read_pathcsv(os.path.join( os.getcwd(), 'post', f))
    comments = []
    for plink in forums_s:
        pagelink = plink
        next_page = True
        while next_page:
            print(plink)
            url_p = url[:-1]+pagelink
            data_p, proxy_pool = find_available_ip(url_p, proxy_pool)
            if data_p is None:
                next_page = False
                print('HTTP Status was not 200.')
                continue
            
            try:
                post = lxml.html.fromstring(data_p.decode('cp1252'))
            except:
                try:
                    post = lxml.html.fromstring(data_p.decode('utf8'))
                except:
                    continue
            try:
                page = post.find('.//li[@class="current"]/a').text
                page = int(page)
                print('#', page)
                print(type(page))
            except:
                print('# 1')
            
            for comment in post.xpath('//div[contains(@id, "post_message_")]'):
                #time.sleep(random.randint(1,3))
                try:
                    comment.find('.//div[@class="quote"]').drop_tree()
                except:
                    pass
                comments.append(str(comment.text_content()))
                print(str(comment.text_content()))
            

            try:
                pagelink = post.xpath('.//a[contains(text(),"Next ›")]')[0].attrib.get('href')
                next_page = True
            except:
                next_page = False
            print('-'*10)
            
            filename = f[:-8] + 'comments.csv'
            write_pathcsv('post/'+filename, 'comments', comments)
    
    filename = f[:-8] + 'comments_all.csv'
    write_pathcsv('post/'+filename, 'comments', comments)