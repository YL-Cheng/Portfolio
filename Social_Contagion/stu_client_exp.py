#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 10 00:04:24 2019

@author: mac
"""

import time
import socket
from psychopy import visual, core, event

confirmation = 'go'

code='utf-8'
c=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(('localhost', 1234)) 
c.settimeout(600)


w = visual.Window(size=[1366,768])
#w = visual.Window(size=[1900,1020])

while confirmation == 'go':
    msg = c.recv(1024).decode(code)
    #if msg == 'ready':
    print('msg:'+ msg)
    visual.TextStim(w, text='請問您認為這個詞彙有多符合類別標籤？',font="Songti SC", pos=(0.0, 0.4), height=0.12).draw()
    visual.TextStim(w, text='一般符合              相當符合              非常符合',font="Songti SC", pos=(0.0, 0.0), height=0.08).draw()
    visual.TextStim(w, text='1     2     3     4     5',font="Songti SC", pos=(0.0, -0.2), height=0.18).draw()
    w.flip()
    t0 = time.time()
    
    for i in range(20):
        r_score = event.waitKeys(keyList = ['1', '2', '3', '4', '5'], maxWait=0.1)
        if r_score != None:
            RT = time.time()-t0
            break
        elif time.time()-t0 >= 4.0:
            break
        else:
            print(i+1)
            print(time.time()-t0)
            opa = 1-0.05*(i+1)
            visual.TextStim(w, text='請問您認為這個詞彙有多符合類別標籤？',font="Songti SC", pos=(0.0, 0.4), height=0.12, opacity=opa).draw()
            visual.TextStim(w, text='一般符合              相當符合              非常符合',font="Songti SC", pos=(0.0, 0.0), height=0.08, opacity=opa).draw()
            visual.TextStim(w, text='1     2     3     4     5',font="Songti SC", pos=(0.0, -0.2), height=0.18, opacity=opa).draw()
            w.flip()
           
    if r_score==None:
        r_score = 'N'
        RT = 'NaN'
        visual.TextStim(w, text='太慢了！',font="Songti SC", height=0.12, bold=True, color=(170, 0, 0), colorSpace='rgb255').draw()
        w.flip()
        core.wait(0.2)
        w.flip()
       
    sendstr = str(r_score[0])+','+str(RT) #
    print(sendstr) #
    
    c.sendall(sendstr.encode(code))
    w.flip()
    
    
    confirmation = c.recv(1024).decode(code)
    print('confirmation:' + confirmation)
       
w.close()
c.close()
