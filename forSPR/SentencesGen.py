#!/usr/bin/env python
#-*- coding:utf-8 -*-
"""
每一行为满足SenProduce.py中定义的句法格式的句子
输入:参数1,输入文法文件；参数2,输出句子文件
"""


from SenProduce import *
import sys


def execute(sourcename, targetname):
    sp = open(sourcename)
    tp = open(targetname, 'w')
    lines = sp.readlines()
    result = []
    for line in lines:
        line = line.replace('\n', '')
        x = DirectGraph(line)
        x.parse()
        result.extend(x.getAllSentences())
    tp.write("生成总句数:%d\n"%len(result))
    for resen in result:
        print resen
        tp.write(resen + '\n')
    sp.close()
    tp.close()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print error
    else:
        print sys.argv[1]
        print sys.argv[2]
        execute(sys.argv[1], sys.argv[2])
