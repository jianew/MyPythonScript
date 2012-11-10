#!/urs/bin/env python
#-*- coding:utf-8 -*-
"""
脚本完成的主要功能是根据文法生成语句,因为需要功能比较简单,文法简单定义如下:
null表示空,字母表=所有汉字U英文字母U(NULL)  sentence=X(Y)Z X=字母表*
Z=字母表* Y=X Y=Z  Y=X|Y
"""


class Alphabet:
    def __init__(self):
        pass
    
    def check(self, char):
        pass


class InStrWra:

    def __init__(self , instring):
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

    def getTrans(self):
        return self.N_transtions

    def getId(self):
        return self.N_nodeid

    def __str__(self):
        string=''
        for node,transtr in self.N_transtions.items():
            string+=transtr+'->'+str(node.getId())+","
        return str(self.N_nodeid)+"     "+string+"\n"


class DirectGraph:

    def __init__(self,instring):
        self.D_stream=InStrWra(instring).getStr()
        self.D_opstack=[]
        self.D_optrstack=[]
        self.D_nodetable=[]

    def parse(self):
        while True:
            #import pdb
            #pdb.set_trace()
            (ss,syb)=self.getUnitString()
            if ss=='' and syb ==None:
                break
            elif ss!='':
                self.push(ss)
            if syb=='(':
                self.D_optrstack.append('(')
            elif syb==')':
                while True:
                    if self.D_optrstack[-1]!='(':
                        if len(self.D_optrstack)!=0 and self.D_optrstack[-1]=='|':
                            self.evalor()
                            self.D_optrstack.pop()
                        elif len(self.D_optrstack)!=0 and self.D_optrstack[-1]=='*':
                            self.evaland()
                            self.D_optrstack.pop()
                    elif  len(self.D_optrstack)!=0:
                        self.D_optrstack.pop()
                        break
            elif syb=='|' or syb=='*':
                while True:
                    if len(self.D_optrstack)!=0 and self.D_optrstack[-1]=='|':
                        self.evalor()
                        self.D_optrstack.pop()
                    elif  len(self.D_optrstack)!=0 and self.D_optrstack[-1]=='*':
                        self.evaland()
                        self.D_optrstack.pop()
                    else:
                        self.D_optrstack.append(syb)
                        break
            elif syb==None:
                break
        while True:
            if len(self.D_optrstack)!=0 and self.D_optrstack[-1]=='|':
                self.evalor()
                self.D_optrstack.pop()
            elif len(self.D_optrstack)!=0 and self.D_optrstack[-1]=='*':
                self.evaland()
                self.D_optrstack.pop()
            else:
                break
        self.D_nodetable=self.D_opstack[0]

    def evalor(self):
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

    def evaland(self):
        dn1=self.D_opstack.pop()
        dn0=self.D_opstack.pop()
        dn0[-1].connect('NULL',dn1[0])
        dn0.extend(dn1)
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
            if syb!='*' and syb!='(' and syb!=')' and syb!='|' and syb!=None:
                ss+=syb
            else:
                break
        return (ss,syb)

    def getAllSentences(self):
        allsentences=[]
        if len(self.D_nodetable)==0:
            print "error"
            return None
        for node,transtr in self.D_nodetable[0].getTrans().items():
            remainstr=self.getFromNodeX(node)
            allsentences.extend(map(lambda x:transtr+x,remainstr))
        allsentences=map(lambda x:x.replace('NULL',''),allsentences)
        return allsentences

    def getFromNodeX(self,node):
        if len(node.getTrans())==0:
            return ['']
        result=[]
        for nextnode,transtr in node.getTrans().items():
            remainstr=self.getFromNodeX(nextnode)
            result.extend(map(lambda x:transtr+x,remainstr))
        return result


if __name__=="__main__":
    x=DirectGraph("我想吃*(蛋糕|饺子|NULL)*和*(蛋糕|饺子)")
    x.parse()
    #import pdb 
    #pdb.set_trace()
    for i in x.getAllSentences():
        print i

    
