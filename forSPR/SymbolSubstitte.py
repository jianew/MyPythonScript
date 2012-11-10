#~/usr/bin/env python
#-*- coding:utf-8 -*-

from SenProduce import *

class SymSentence:

    def __init__(self, instr):
        self.S_head = instr[:instr.find('=')].split(' ')
        self.S_body = instr[instr.find('=')+1:].split(' ')

    def getHead(self):
        return self.S_head

    def getBody(self):
        return self.S_body


class SymSentences:
    
    def __init__(self,lines):
        self.S_nos={}
        self.S_iss=[]
        for line in lines:
            line.replace('\n', 0)
            tempsen = SymSentence(line)
            if tempsen.getHead() != "S":
                self.S_nos["{"+tempsen.getHead()+"}"] = tempsen.getBody()
            else:
                self.S_iss.append[tmepsen.getBody()]

    def getSentencePro(self):
        sentencepros=[]
        for i in self.S_iss:
            sentencepros.append(self.generate(i))

    def generate(self,Synsenpro):
        
        
            
