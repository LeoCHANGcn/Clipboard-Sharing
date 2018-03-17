#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:40:30 2018

@author: ZhangShichao
<zhangshichaochina@gmail.com>

"""

import clipboard as cpb
import socket 
import time
from argparse import ArgumentParser


class NetClipboard():
    '''
    Share your clipboard between 2 computers at the same wlan.
    '''
    def __init__(self):
        '''
        '''
        self.clip = cpb.paste()
        
        self.parse = ArgumentParser(description=' Share clipboard between two computers.\n Only share raw string text.')
        self.parse.add_argument('-a',
                                '--address',
                                default="0.0.0.0",
                                help="Set the IP of another computer.")
        self.parse.add_argument('-i',
                                '--interval',
                                type=float,
                                default=0.1,
                                help='Interval time between every copy/paste by seconds.(can be float number)')
        self.parse.add_argument('-l',
                                '--length',
                                type=int,
                                default=8192,
                                help='Maximum length of the string')
        self.parse.add_argument('-p',
                                '--port',
                                type=int,
                                default=6666,
                                help='Specify the port of another computer')
        self.option, self.content = self.parse.parse_known_args()
        
    def clipShare(self):
        '''
        Send the content of current clipboard to another side.
        '''
        #print(self.option.address, self.option.port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.option.address, self.option.port))
        while True:
            tmp = cpb.paste()
            if tmp != self.clip:
                self.clip = tmp
                self.s.send(self.clip.encode())
            else:  
                self.s.send("0".encode())
            tmp = self.s.recv(self.option.length).decode()
            if tmp == "0" or tmp == "1":
                pass
            elif tmp != self.clip:
                self.clip = tmp
                cpb.copy(self.clip)
            
            time.sleep(self.option.interval)
        self.s.close()

if __name__ == "__main__":
    '''
    Run the netClip application.
    '''
    clip = NetClipboard()
    while True:
        clip.clipShare()
