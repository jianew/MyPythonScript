#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
脚本功能用来分析语音识别结果的ser和wer,需要传入参数ser_thresold来得到ser
"""


import sys,getopt
from werget import *
from pylab import *

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
    def getOLength(self):
        return len(self.origin)
    def __getitem__(self,key):
        if key==0:
            return self.origin
        else:
            return self.reres
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
        thresold=float(thresold)
        #for i in self.a_senparis:
         #   print i.getWER()
        #print filter(lambda x: x.getWER()>thresold,self.a_senparis)
        return len(filter(lambda x: x.getWER()>thresold,self.a_senparis))/float(len(self.a_senparis))
    def getLengthWerPairs(self):
        return map(lambda x:(x.getOLength(),x.getWER()),self.a_senparis)
    def printREPORT(self,ser_thresolf):
        print "平均wer:% .2f%%"%(100*self.getAvaWER())
        print "ser:% .2f%%"%(100*self.getSER(ser_thresolf))
        print '\n\n'
        for index,pair in enumerate(self.a_senparis):
            print "%d.%s"%(index,str(pair))
    
    def printREPORTinFile(self,ser_thresolf,filename):
        fp=open(filename,'w')
        fp.write("平均wer:% .2f%%\n"%(100*self.getAvaWER()))
        fp.write("ser:% .2f%%\n"%(100*self.getSER(ser_thresolf)))
        fp.write('\n\n')
        for index,pair in enumerate(self.a_senparis):
            fp.write("%d.%s\n"%(index,str(pair)))
        fp.close()
    def printSortedParisInfile(self,ser_thresolf,filename):
        fp=open(filename,'w')
        fp.write("平均wer:% .2f%%\n"%(100*self.getAvaWER()))
        fp.write("ser:% .2f%%\n"%(100*self.getSER(ser_thresolf)))
        fp.write('\n\n')
        for index,pair in enumerate(sorted(self.a_senparis,key=lambda x:len(x[0]))):
            fp.write("原句长度:%d\n%s\n"%(len(pair[0]),str(pair)))
        fp.close()        
    def plotLengthWerPairs(self,graphname):
        paris=self.getLengthWerPairs()
        xy=sorted(paris,key=lambda x:x[0])
        x=[]
        y=[]
        sumwer=0
        sumkeynums=0
        keyiter=xy[0][0]
        for key,wer in xy:
            if key==keyiter:
                sumwer+=wer
                sumkeynums+=1
            else:
                x.append(keyiter)
                keyiter=key
                #print sumwer
                #print sumkeynums
                y.append(sumwer/sumkeynums)
                sumwer=wer
                sumkeynums=1         
        scatter(x,y)
        savefig(graphname,dpi=480)
    


if __name__=="__main__":
    opts,args=getopt.getopt(sys.argv[1:],"s:i:o:")
    ser_thresold=0
    infile=""
    outfile=""
    for op,value in opts:
        if op=="-s":
            print value
            ser_thresold=value
        if op=="-i":
            print value
            infile=value
        if op=="-o":
            print value
            outfile=value
    ana=Analyze(infile)
    ana.printREPORT(ser_thresold)
    ana.printREPORTinFile(ser_thresold,outfile)
    ana.printSortedParisInfile(ser_thresold,outfile.replace('.txt','')+"_sorted.txt")
    ana.plotLengthWerPairs(outfile.replace('.txt','')+".png")

            
                
                
                
