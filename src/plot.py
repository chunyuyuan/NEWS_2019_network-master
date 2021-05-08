#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 17:28:34 2017

@author: Moti
"""

# libraries and data


import random
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import os
import gc

def Cal(ex,this):
    #print this
    counter = []
    for i in range(len(this)):
        counter.append(1)
    for i in range(len(this)) :
        counter[i] = 1
        for types in ex :
            for p in types :
                if this[i]==p:
                    counter[i] = counter[i]+1
    res = []
    for i in range(6):
        temp = []
        for j in range(len(this)):
            if(i+1 == counter[j]):
                temp.append(this[j])
        if len(temp)==0 :
            temp.append(-1)
        res.append(temp)
    
    return res

def main(from_date,to_date,path,X,Temperature, Discharge,pwps):#,Major_Tributary):
    #print "poWWWWWWEr :",pwps
    #from_date = "Nov 23 2017"
    #to_date = "Dec 1 2017"
    #fig = figure()
    # fake inputs #################################################################
     
    #N = 50
    #Discharge = [450+(200*random.random()) for i in range(N)]
    #Temperature = [40*random.random() for i in range(N)]
    #Discharge.sort()
    #Temperature.sort()
    #X = [int(100*random.random()) for i in range(N)]
    #X.sort()
    
    
    # plt #######################################################3#################
    #plt.style.use('fivethirtyeight')
    #plt.style.use('seaborn-darkgrid')
    #print "main step1"
    sns.set_style ("darkgrid")
    sns.set_color_codes("muted")
    #sns.set_style("darkgrid")
    #sns.set(style ='darkgrid', rc={"grid.linewidth": 0.5})
    #print "main step4"
    sns.set_context("paper", rc={"font.size":7,"axes.titlesize":8,"axes.labelsize":2})  
    #print "main step5"
    my_dpi=100
    plt.figure(figsize=(6, 4), dpi=my_dpi)
    #print "main step3"
    #fig = plt.figure()
    #plt = fig.add_subplot(111)
    fig, plt1 = plt.subplots() 
    plt1 = plt.gca()
    plt2 = plt1.twinx()
    #print "main step2.1"
    # Now re do the interesting curve, but biger with distinct color
    D = plt1.plot(X, Discharge, marker='', color='lightblue', linewidth=4, alpha=0.7, label = 'Discharge')
    T = plt2.plot(X, Temperature, marker='', color='darkred', linewidth=2, alpha=0.7 ,label = 'Temperature')
    
    
    plt1.grid(None)
    plt1.set_xlim(min(X),max(X))
   
    
    plt1.set_ylim(min(Discharge),max(Discharge))
    plt2.set_ylim(min(Temperature), max(Temperature))
    length = max(Discharge)-min(Discharge)
    
    #PLOT PWP #####################################################################
    #fig, ax1 = plt.subplots()
    
    #pwps= [[40,6],[40,2],[40,3],[50,1],[70,4],[70,6],[70,2],[80,5],[5,2],[5,3]]
    ST_OT, ST_RC,ST_DC,CC_OT,CC_RC,CC_DC = [],[],[],[],[],[]
    #print "main step2"
    for row in pwps:
        if(int(row[1])==1):
            ST_OT.append(row[0])   
        elif(int(row[1])==2):
            ST_RC.append(row[0]) 
        elif(int(row[1])==3):
            ST_DC.append(row[0]) 
        elif(int(row[1])==4):
            CC_OT.append(row[0]) 
        elif(int(row[1])==5):
            CC_RC.append(row[0]) 
        elif(int(row[1])==6):
            CC_DC.append(row[0]) 
            
    #print "testtt",CC_RC
    #OTC_P = plt2.plot(OTC_PLANTS,Z, marker='^', markersize = 5, linestyle='None', color ='black',label = 'OTC Plant')
    #RTC_P = plt2.plot(RTC_PLANTS,Z, marker='^', markersize = 5, linestyle='None', color ='gray',label = 'RTC Plant')
    #flatui = ["#9b59b6", "#3498db", "#95a5a6", "#e74c3c", "#34495e", "#2ecc71"]
    
    ## 1ST ####
    height = length/70
    tall = 10
    ST_OT_P = plt2.plot(ST_OT,[height for i in range(len(ST_OT))], marker='o', markersize = 5, linestyle='None', color ='turquoise',label = 'ST_OT Plant',markerfacecolor= 'None',markeredgewidth=1)
    
    ## 2ND ####
    res = Cal([ST_OT],ST_RC)
    #print "2::",res
    flag = True
    for g in range(len(res)) :
        if res[g][0] != -1:
            if (flag):
                ST_RC_P = plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='^', markersize = 5, linestyle='None', color ='turquoise',label = 'ST_RC Plant', markerfacecolor='None', markeredgewidth=1 )
                flag = False
            else:
                plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='^', markersize = 5, linestyle='None', color ='turquoise',label = 'ST_RC Plant', markerfacecolor='None', markeredgewidth=1 )
    #CC_RC_P = plt2.plot(CC_RC,[height+10 for i in range(len(CC_RC_up))], marker='^', markersize = 10, linestyle='None', color ='turquoise',label = 'CC_RC Plant', markerfacecolor='lightgreen', markeredgewidth=3 )
    
    ## 3RD ####
    res = Cal([ST_OT,ST_RC],ST_DC)
    #print "3::",res
    flag = True
    for g in range(len(res)) :
        if res[g][0] != -1:
            if(flag):
                ST_DC_P = plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='s', markersize = 5, linestyle='None', color ='turquoise',label = 'ST_DC Plant', markerfacecolor= 'None', markeredgewidth=1)
                flag = False
            else:
                plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='s', markersize = 5, linestyle='None', color ='turquoise',label = 'ST_DC Plant', markerfacecolor= 'None', markeredgewidth=1)
    #CC_DC_P = plt2.plot(CC_DC,[height for i in range(len(CC_DC))], marker='s', markersize = 10, linestyle='None', color ='turquoise',label = 'CC_DC Plant', markerfacecolor= 'None', markeredgewidth=1)
    
    ## 4 ####
    res = Cal([ST_OT,ST_RC, ST_DC],CC_OT)
    #print CC_OT,"4::",res
    flag = True
    for g in range(len(res)) :
        if res[g][0] != -1:
            if (flag):
                CC_OT_P = plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='o', markersize = 5, linestyle='None',  color ='darkblue',label = 'CC_OT Plant',markerfacecolor= 'None', markeredgewidth=1)
                flag = False
            else:
                plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='o', markersize = 5, linestyle='None',  color ='darkblue',label = 'CC_OT Plant',markerfacecolor= 'None', markeredgewidth=1)
    
    #ST_OT_P = plt2.plot(ST_OT,[height for i in range(len(ST_OT))], marker='o', markersize = 10, linestyle='None',  color ='darkblue',label = 'ST_OT Plant',markerfacecolor= 'None', markeredgewidth=1)
    #ST_RC_P = plt2.plot(ST_RC,[1.3 for i in range(len(ST_RC))], marker='o', markersize = 10, linestyle='None', color ='gray',label = 'ST_RC Plant', markerfacecolor= 'None')
    ## 5 ####
    res = Cal([ST_OT,ST_RC, ST_DC,CC_OT],CC_RC)
    #print "5::",res
    flag = True
    for g in range(len(res)) :
        if res[g][0] != -1:
            if(flag):
                #print "lll",g
                CC_RC_P = plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='^', markersize = 5, linestyle='None', color ='darkblue',label = 'CC_RC Plant',markerfacecolor='None', markeredgewidth=1)
                flag= False
            else:
                plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='^', markersize = 5, linestyle='None', color ='darkblue',label = 'CC_RC Plant',markerfacecolor='None', markeredgewidth=1)
    
    #ST_RC_P = plt2.plot(ST_RC,[height for i in range(len(ST_RC))], marker='^', markersize = 10, linestyle='None', color ='darkblue',label = 'ST_RC Plant',markerfacecolor='darkblue', markeredgewidth=3)
    
    ## 6 ####
    res = Cal([ST_OT,ST_RC, ST_DC,CC_OT,CC_RC], CC_DC)
    #print "6::",res
    flag = True
    for g in range(len(res)) :
        if res[g][0] != -1:
            if(flag):
                CC_DC_P = plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='s', markersize = 5, linestyle='None', color='darkblue',label = 'CC_DC Plant', markerfacecolor= 'None', markeredgewidth=1)
                flag = False
            else:
                plt2.plot(res[g],[(g+1)*height for i in range(len(res[g]))], marker='s', markersize = 5, linestyle='None', color='darkblue',label = 'CC_DC Plant', markerfacecolor= 'None', markeredgewidth=1)
    
    #ST_DC_P = plt2.plot(ST_DC,[height for i in range(len(ST_DC))], marker='s', markersize = 10, linestyle='None', color='darkblue',label = 'ST_DC Plant', markerfacecolor= 'None', markeredgewidth=1)
    
    
    # ADD Vertical Lines ##########################################################
    #Major_Tributary = [10, 30, 70]
    LINE= []
    Temp = []
  #  for i in range(len(Major_Tributary)):
      #  if i==0:
      #      Temp.append(plt2.axvline(Major_Tributary[i], color='gray',linestyle='--', label = 'Major_Tributary'))
       # else:
       #     LINE.append(plt2.axvline(Major_Tributary[i], color='gray',linestyle='--', label = '_nolegend_'))
        
    
        
    # ADD LEGEND ##################################################################
    if(len(pwps)!=0):
        lns = D + T + ST_OT_P + ST_RC_P + ST_DC_P + CC_OT_P + CC_RC_P + CC_DC_P + Temp
    else:
        lns = D + T + Temp
    #print lns
    labs = [lns[i].get_label() for i in range(len(lns))]
    lgd = plt2.legend(lns, labs, loc='upper left', bbox_to_anchor=(1.1,1))
    #print lns[0].get_xdata()
    print labs
    ###print lns[0].get_ydata()
    #print "\n"
    #print lns[1].get_xdata()
    #print "\n"
    #print lns[1].get_ydata()
    str1ist1=' '.join(str(x) for x in lns[0].get_xdata() )
    str1ist2=' '.join(str(x) for x in lns[0].get_ydata() )
    str1ist3=' '.join(str(x) for x in lns[1].get_ydata() )
    
    
    # ADD Title and Labels ########################################################
    plt1.set_xlabel('Distance From start to end (km)')
    plt1.set_ylabel('Average Discharge ($m^3/s$)', color='lightblue')
    #plt2.set_ylabel('Tempreture (°C)', color='darkred')
    plt2.set_ylabel(u"Average Water Temperature (\N{DEGREE SIGN} C)", color='darkred')
    
    plt1.xaxis.label.set_size(10)
    plt1.yaxis.label.set_size(10)
    plt2.yaxis.label.set_size(10)
    
    #print D.data()
    #print (lns-D)
    
    plt1.tick_params(axis='y', colors='lightblue', which='both')
    plt2.tick_params(axis='y', colors='darkred', which='both')
    
    #SAVE ########################################################################
    art = []
    art.append(lgd)
    #dir = os.path.dirname(__file__)
    #import time
    #before = time.time()
    #filename = os.path.join(dir, 'plot.png')
    #plt.savefig(
        #filename, additional_artists=art,
        #bbox_inches="tight")
    
    figfile = BytesIO()
    
    plt.savefig(figfile, format='png',additional_artists=art,
        bbox_inches="tight")
    figfile.seek(0)
    ##figdata_png = base64.b64encode(figfile.getvalue())
    plt.close('all')

    gc.collect()
    return figfile,str1ist1,str1ist2,str1ist3

