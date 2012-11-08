#!/usr/bin/env python
#-*- coding:utf-8 -*-
from werget import *
def DelUnneccSymbols(sentence):
    symboltable=[':',' ',',','.',',','.',' ','\n','\r','：','，','.']
    for symbol in symboltable:
        sentence=sentence.replace(symbol,'')
    return sentence
class SenPair:
    def __init__(self,sent1,sent2):
        self.origin=sent1
        self.reres=sent2
    def getEditDistance(self):
        return mini_edit_distance(self.origin,self.reres,1,1,1)
    def getWER(self):
        return self.getEditDistance()/float(len(self.origin))
    def __str__(self):
        #return "原句:"+self.origin+"\n"+"识别结果:"+self.reres+"\n"+"wer:"+"%.4f"%(100*self.getWER()))+"\n"
        return "原句:%s \n识别结果:%s \n wer: %.2f%% \n"%(self.origin,self.reres,100*self.getWER())
        
class Analyze:
    def __init__(self,filepath):
        self.a_senparis=[]
        fp=open(filepath)
        lines=fp.readlines()
        linesnum=len(lines)
        lp=0
        while lp<linesnum:
            line=lines[lp]
            if line.find("原句")!=-1:
                line=line[line.find("原句"):]
                line=line.replace("原句",'')
                line=DelUnneccSymbols(line)
                sent1=line
                lp+=1
                if lp==linesnum:
                    break
                line=lines[lp]
                while line.find("NULL")!=-1 and line.find("识别结果")!=-1:
                    lp+=1
                    if lp==linesnum :
                        break
                    line=lines[lp]
                if line.find("识别结果")==-1:
                    print "unexpected error"
                line=line[line.find("识别结果"):]
                line=line.replace("识别结果",'')
                line=DelUnneccSymbols(line)
                sent2=line
                self.a_senparis.append(SenPair(sent1,sent2))
                lp+=1
    def __str__(self):
        return reduce(lambda x,y:str(x)+str(y),self.a_senparis)
    def getAvaWER(self):
        return reduce(lambda x,y:x+y,map(lambda x:x.getWER(),self.a_senparis))/len(self.a_senparis)
    def getSER(self,thresold):
        return len(filter(lambda x: x.getWER()>thresold,self.a_senparis))/float(len(self.a_senparis))
    def printREPORT(self,ser_thresolf):
        print "平均wer:% .2f%%"%self.getAvaWER()
        print "ser:% .2f%%"%self.getSER(ser_thresolf)
        print '\n\n'
        for index,pair in enumerate(self.a_senparis):
            print "%d.%s"%(index,str(pair))
if __name__=="__main__":
    filepath1=r'/home/liuzh/workspace/test_report/log1/r1.txt'
    ana=Analyze(filepath)
    ana.printREPORT(0)

            
                
                
                
