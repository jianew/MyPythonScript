# !/usr/bin/env python
#-*- coding:utf-8 -*-
def mini_edit_distance(stringa,stringb,ins_cost,subst_cost,del_cost):
    n=len(stringa)
    m=len(stringb)
    distance=[[0 for i in range(m+1)] for j in range(n+1)]
    for i in range(1,n+1):
        distance[i][0]=distance[i-1][0]+ins_cost
    for j in range(1,m+1):
        distance[0][j]=distance[0][j-1]+del_cost
    for i in range(1,n+1):
        for j in range(1,m+1):
            if stringa[i-1]==stringb[j-1]:
                distance[i][j]=distance[i-1][j-1]
            else:
                distance[i][j]=min(distance[i-1][j]+ins_cost,distance[i-1][j-1]+subst_cost,distance[i][j-1]+del_cost)
    return distance[n][m]
if __name__=="__main__":
    stringa="intention"
    stringb="execution" 
    print mini_edit_distance(stringa,stringb,1,1,1)
