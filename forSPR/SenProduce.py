#!/urs/bin/env python
#-*- coding:utf-8 -*-
""
#脚本完成的主要功能是根据文法生成语句,因为需要功能比较简单,文法简单定义如下:
#null表示空,字母表=所有汉字U英文字母U(NULL)  sentence=X(Y)Z X=字母表* 
#Z=字母表* Y=X Y=Z  Y=X|Y
""

class Alphabet:
    def __init__(self):
        pass
    def check(self,char):
        pass
class InStrWra:
    def __init__(self,instring):
        self.i_sentences=instring
    def getStr(self):
        for char in self.i_sentences:
            yield char
        yield None
class Node:
    SN_nodeid=0
    def __init__(self):
        self.N_nodeid=self.__class__.SN_nodeid
        self.__class__.SN_nodeid+=1
        self.N_transtions={}
    def connect(self,transtr,node):
        self.N_transtions[node]=transtr
class DirectGraph:
    def __init__(self,instring):
        self.D_stream=InStrWra(instring).getStr()
        self.D_opstack=[]
        self.D_optrstack=[]
        self.D_nodetable=[]
    def parse():
        while True:
            (ss,syb)=self.getUnitString()
            if ss=='' and syb ==None:
                break
            elif ss!='':
                push(ss)
            if syb=='(':
                self.D_optrstack.append('(')
            elif syb==')':
                while True:
                    if self.D_optrstack[-1]!='(':
                        self.eval()
                    else:
                        self.D_optrstack.pop()
                        break
            elif syb=='|':
                while True:
                    if self.D_optrstack[-1]=='|':
                        self.eval()
                    self.D_optrstack.pop()
    def eval(self):
        dn1=self.D_opstack.pop()
        dn0=self.D_opstack.pop()
        s0=Node()
        s1=Node()
        s0.connect('NULL',dn0[0])
        s0.connect('NULL',dn1[0])
        dn0[-1].connect('NULL',s1)
        dn1[-1].connect('NULL',s1)
        dn0.extend(dn1)
        dn0.insert(0,s0)
        dn0.append(s1)
        self.D_opstack.append(dn0)            
    def push(self,ss):
        node1=Node()
        node2=Node()
        node1.connect(ss,node2)
        self.D_opstack.append([node1,node2])    
    def getUnitString(self):
        ss=''
        while True:
            syb=self.D_stream.next()
            if syb!='(' and syb!=')' and syb!='|' and syb!=None:
                ss+=syb
            else:
                break
        return (ss,syb)
                
if __name__=="__main__":
    pass
