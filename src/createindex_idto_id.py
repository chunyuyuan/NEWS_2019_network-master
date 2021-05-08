
import io
import base64
import csv
import json
from collections import OrderedDict
import numpy 
import pandas as pd
from numpy import genfromtxt



##initial netwrok csv data############################
rawdata=open('NetworkWithDistance.txt') 

my_data=genfromtxt('networkwithdist.csv',delimiter=',')
#my_data=numpy.delete(my_data,(0),axis=0)
header=['id','id_to','lon','lat','basinid']
frame=pd.DataFrame(my_data,columns=header)

x=frame['id']
x[0]

x[0]
data=[]
i=0
myfile = open('tempcsv.csv', mode='wt')
while(i<len(x)):
  temp=[]
  y=frame.ix[frame['id_to']==x[i]]
  j=0
  while(j<len(y)):
    xx=y.loc[y.index[j]]
    temp.append(xx['id'])
    j+=1
  if(len(temp)>=0) :
    
    s=str(x[i])
    t=0
    while(t<len(temp)):
      s+=','+str(temp[t])
      t+=1
    s+='\n'
    
    myfile.write(s)
  i+=1
  print i, x[i]


myfile.close