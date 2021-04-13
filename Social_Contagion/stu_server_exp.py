#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 00:04:12 2019

@author: mac
"""
import time
import socket
import random
import pandas as pd
import matplotlib.pyplot as plt
from psychopy import core
from pydub import AudioSegment
from pydub.playback import play


## Connecting ##

mat_stu = pd.read_excel('Study List.xlsx')


play_order = []
for i in range(len(mat_stu['ID'])):
    play_order.append(i)
random.shuffle(play_order)

data_s = pd.DataFrame()
        
code='utf-8'
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind(('localhost', 1234))
s.listen(1)
s.settimeout(1800)

(c,adr)=s.accept() 
print('Client:',c,adr)


## Type ID ##

group = input('group: ') # A or B or C
num = input('num: ')
condition = input('condition: ') # 1,2,3,4,5,6

# =============================================================================== #

## Study Phase ##

for i in play_order:
    trial = AudioSegment.from_wav('./2.2.Record/{}.wav'.format(i+1))
    core.wait(0.3+1.2*random.random())
    play(trial)
    c.sendall(('ready').encode(code))
    c.settimeout(120)
    
    recvstr = c.recv(1024).decode(code)
    print(recvstr)
    r_score,RT = recvstr.split(',')
    
    
    it_stu = pd.Series([mat_stu['ID'][i],mat_stu['item'][i],mat_stu['category'][i], r_score, RT])
    data_s = data_s.append(it_stu, ignore_index=True)
    
    c.sendall(('go').encode(code))

c.sendall(('done').encode(code))

s.close()

data_s.columns = ['ID','item', 'category', 'score', 'RT']

data_s.to_excel('../raw/({0}{1}_{2}) stu_{3}.xlsx'.format(group, num, condition, time.strftime("%Y%m%d-%H%M")))

# =============================================================================== #

data_s2 = data_s.replace('NaN','')
data_s2 = data_s2.replace('N','')

data_s2['RT'] = data_s2['RT'].apply(pd.to_numeric)
data_s2['score'] = data_s2['score'].apply(pd.to_numeric)


fig = plt.figure(figsize=(10,6))

ax1 = plt.gca()
ax1.bar(data_s2['ID'],data_s2['RT'])
ax1.set_ylim(0,2.7)


ax2 = ax1.twinx()
ax2.scatter(data_s2['ID'],data_s2['score'], c='r', alpha=0.5)
ax2.set_ylim(0.5,5.5)

plt.title('{0}{1}_{2}   RT: {3}'.format(group, num, condition, data_s2['RT'].mean()))
plt.show()
