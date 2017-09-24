#!/usr/bin/env python
# -*- coding: utf-8 -*- 
#Created by Dagger -- https://github.com/DaggerES

def Xor(buf):
    cccam = "CCcam"
    for i in range(0, 8):
        buf[8 + i] = 0xff & (i * buf[i])
        if i < 5:   
            buf[i] ^= ord(cccam[i])
    return buf

class CryptographicBlock(object):
    def __init__(self):
        self._keytable = [0] * 256
        self._state = 0
        self._counter = 0
        self._sum = 0

    def Init(self, key, len):
        for i in range(0, 256):
            self._keytable[i] = i
        j = 0
        for i in range(0, 256):
            j = 0xff & (j + key[i % len] + self._keytable[i])
            self._keytable[i], self._keytable[j] = self._keytable[j], self._keytable[i]
        self._state = key[0]
        self._counter = 0
        self._sum = 0

    def Decrypt(self, data, len):
        for i in range(0, len):
            self._counter = 0xff & (self._counter + 1)
            self._sum = self._sum + self._keytable[self._counter]

            #Swap keytable[counter] with keytable[sum]
            self._keytable[self._counter], self._keytable[self._sum & 0xFF] = \
                self._keytable[self._sum & 0xFF], self._keytable[self._counter]

            z = data[i]
            data[i] = z ^ self._keytable[(self._keytable[self._counter] + \
                self._keytable[self._sum & 0xFF]) & 0xFF] ^ self._state
            z = data[i]
            self._state = 0xff & (self._state ^ z)

    def Encrypt(self, data, len):
        for i in range(0, len):
            self._counter = 0xff & (self._counter + 1)
            self._sum = self._sum + self._keytable[self._counter]
            
            #Swap keytable[counter] with keytable[sum]
            self._keytable[self._counter], self._keytable[self._sum & 0xFF] = \
                self._keytable[self._sum & 0xFF], self._keytable[self._counter]

            z = data[i]
            data[i] = z ^ self._keytable[(self._keytable[self._counter & 0xFF] + \
                self._keytable[self._sum & 0xFF]) & 0xff] ^ self._state

            self._state = 0xff & (self._state ^ z)
