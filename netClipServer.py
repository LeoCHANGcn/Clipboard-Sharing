#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 16 21:40:30 2018

@author: ZhangShichao
<zhangshichaochina@gmail.com>

"""

import clipboard as cpb
import subprocess as sbp
import socket
import time
import os
from argparse import ArgumentParser


class NetClipboard():
    '''
    Share your clipboard between 2 computers at the same wlan.
    '''
    def __init__(self):
        '''
        '''
        self.path = os.getcwd()
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
                                default=6000,
                                help='Specify the port of another computer')
        self.option, self.content = self.parse.parse_known_args()
        if "clip.txt" in os.listdir(self.path):
            pass
        else:
            os.mknod('clip.txt')

    def clipShare(self):
        '''
        Send the content of current clipboard to another side.
        '''

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('0.0.0.0', self.option.port))
        s.listen()
        sock, address = s.accept()

        while True:
            tmp = cpb.paste()
            if tmp != self.clip:
                self.clip = tmp
                sock.send(self.clip.encode('utf-8'))

            tmp = sock.recv(self.option.length).decode('utf-8')

            if tmp == "0" or tmp == '00':
                sock.send("0".encode('utf-8'))
            elif tmp != self.clip:
                self.clip = tmp

                with open(os.path.join(self.path,"clip.txt"), 'w', encoding='utf-8') as f:
                    f.write(self.clip)
                    f.close()
                clipPath = os.path.join(self.path,"clip.txt")
                sbp.call("xclip -sel c < " + clipPath, shell=True)
                #cpb.copy(self.clip)
                sock.send("0".encode('utf-8'))
            else:
                sock.send("1".encode('utf-8'))

            time.sleep(self.option.interval)
        s.close()


if __name__ == "__main__":
    '''
    Run the netClip application.
    '''
    clip = NetClipboard()
    while True:
        clip.clipShare()

