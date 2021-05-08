#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 00:57:51 2017

@author: Moti
"""

#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 11:21:10 2017

@author: Moti
"""
import csv
import numpy as np
from collections import deque
import math
from datetime import datetime
import os
import netCDF4
import matplotlib.pyplot as plt
from vincenty import vincenty
import glob
import re
import datetime as dt
import pandas as pd

#BFS ##########################################################################
###############################################################################
def bfs_shortest_path(Data, Adja, st, gl):
    #print "bfs"
    start = np.array(st)
    goal = np.array(gl)
     
    queue = deque([start])
    while queue:
        node = queue.pop()
        try:
            neighbours = Adja[tuple(node)]
        except KeyError:
            neighbours= []
        for neighbour in neighbours:
            neighbour_info = Data[tuple(neighbour)]
            if(neighbour_info[0]==False):
                queue.append(neighbour)
                update = []
                update.append(True)
                update.append(node[0])
                update.append(node[1])
                update.append(neighbour_info[3])
                Data[tuple(neighbour)] = update
                if (neighbour[0]==goal[0] and neighbour[1] == goal[1]):
                    return True

    return False

#find the path ################################################################
###############################################################################
def get_path(Data, start, goal):
    #print "get path"
    path = []
    order = []
    path.append(goal)
    current = goal
    while (current[0] != start[0] and current[1] != start[1]):
        temp = Data[current]
        current = (temp[1],temp[2])
        path.append(current)
        order.append(temp[3])
    path.append(start)
    return [list(reversed(path)), list(reversed(order))]

###############################################################################
def datetoday(start):
    import datetime
    x = datetime.date(start[0], start[1], start[2])
    #x = date(2004, 1, 23)
    day_of_year = (x - datetime.date(x.year, 1, 1)).days + 1
    return day_of_year

def partial_mean(start,end,path):
    pathmean = []
    startIndex = datetoday(start)
    endIndex   = datetoday(end)
    dir = os.path.dirname( __file__ )
    filename = os.path.join(dir, '*.nc')
    listt = glob.glob(filename)
    for items in listt:
        #print items
        if (str(start[0]) in items and "Discharge" in items):
            filename = os.path.join(dir, items)
            nc = netCDF4.Dataset(filename)
            discharge = nc.variables['discharge']
            for node in path:
                data = discharge[startIndex:endIndex, node[1], node[0]]
                data = np.array(data)
                pathmean.append((endIndex-startIndex+1)*data.mean())
            return [pathmean, (endIndex-startIndex+1)]
    return ([0], 1)


def mean_discharge(path,startdate, enddate):
    #print "mean discharge"
    mean = []
    start,end = startdate.split("-"), enddate.split("-")
    start,end = [int(i) for i in start], [int(i) for i in end]
    weight = []
    if(start[0]==end[0]):
        temp = partial_mean(start,end,path)
	#print "ooooo",temp
        mean.append(temp[0])
        weight.append(temp[1])
    else:
        for i in range(int(start[0]),int(end[0])):
            if(i == start[0]):
                temp = partial_mean(start,[i,12,31],path)
                mean.append(temp[0])
                weight.append(temp[1])
            elif(i == end[0]):
                temp = partial_mean([i,1,1],end,path)
                mean.append(temp[0])
                weight.append(temp[1])
            else:
                temp = partial_mean([i,1,1],[i,12,31],path)
                mean.append(temp[0])
                weight.append(temp[1])
    weight = np.array(weight)
    y = pd.DataFrame(mean)
    y = y.append(pd.DataFrame([y.loc[:][i].sum() for i in range(len(path))]).T, ignore_index=True)
    count = weight.sum()
    res = np.array(y.loc[len(y)-1])/count
    return res
     

#Mean temperature time period #################################################
###############################################################################
def partial_mean1(start,end,path):
    pathmean = []
    startIndex = datetoday(start)
    endIndex   = datetoday(end)
    dir = os.path.dirname( __file__ )
    filename = os.path.join(dir, '*.nc')
    listt = glob.glob(filename)
    for items in listt:
        if (str(start[0]) in items and "airtemperature" in items):
            filename = os.path.join(dir, items)
            nc = netCDF4.Dataset(filename)
            temperature = nc.variables['AirTemperature']
            for node in path:
                data = temperature[startIndex:endIndex, node[1], node[0]]
                data = np.array(data)
                pathmean.append((endIndex-startIndex+1)*data.mean())
            return [pathmean, (endIndex-startIndex+1)]


def mean_temperature(path,startdate, enddate):
    #print "mean temperature"
    mean = []
    start,end = startdate.split("-"), enddate.split("-")
    start,end = [int(i) for i in start], [int(i) for i in end]
    weight = []
    if(start[0]==end[0]):
        temp = partial_mean1(start,end,path)
        mean.append(temp[0])
        weight.append(temp[1])
    else:
        for i in range(int(start[0]),int(end[0])):
            if(i == start[0]):
                temp = partial_mean1(start,[i,12,31],path)
                mean.append(temp[0])
                weight.append(temp[1])
            elif(i == end[0]):
                temp = partial_mean1([i,1,1],end,path)
                mean.append(temp[0])
                weight.append(temp[1])
            else:
                temp = partial_mean1([i,1,1],[i,12,31],path)
                mean.append(temp[0])
                weight.append(temp[1])
    weight = np.array(weight)
    y = pd.DataFrame(mean)
    y = y.append(pd.DataFrame([y.loc[:][i].sum() for i in range(len(path))]).T, ignore_index=True)
    count = weight.sum()
    res = np.array(y.loc[len(y)-1])/count
    return res
###############################################################################
#Find Powerplants in the path #################################################
###############################################################################
def find_pwp(path,dis):
    #print "powerplants"
    pwps = []
    dataset = {}
    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, 'powerplants.csv')
    #with open("/Users/Moti/Documents/NEWS/powerplants.csv") as csvfile:
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                dataset[(int(math.floor((float(row['longitude'])+138)/0.05)), int(math.floor((float(row['longitude'])-5)/0.05)))].append(row['cooling'])   
            except KeyError:
                dataset[(int(math.floor((float(row['longitude'])+138)/0.05)), int(math.floor((float(row['longitude'])-5)/0.05)))]= [row['cooling']]   
    for i in range(len(path)):
        node = path[i]
        try:
            pwps.append(dataset[(node)])
        except KeyError:
            q = 10
    return pwps

#Find major tribs in path #####################################################
###############################################################################
#def major_trib(order, dis):
   # major = []
   # previous = order[0]
   # treshold = 1
   # for i in range(1,len(order)):
    #    if(order[i]>=previous+treshold):
      #      major.append(dis[i])
      #  previous = order[i]
   # return major


#Calculate distance from start to goal ########################################
###############################################################################
def get_distance(lat1, lon1, lat2, lon2): 
    radius = 6371  # km

    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat / 2) * math.sin(dlat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dlon / 2) * math.sin(dlon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = radius * c

    return d
def dis_in_km(path):
    #print "distance"
    dis = [0]
    SUM = 0
    epsilon = 0.000001
    start = path[0]
    last = [(float)(5*start[0])/100 - 138, (float)(5*start[1])/100 + 5]
    prelast = [(float)(5*start[0])/100 - 138, (float)(5*start[1])/100 + 5]
    for i in range(1,len(path)):
        node = path[i]
        this = [(float)(5*node[0])/100 - 138, (float)(5*node[1])/100 + 5]
        #temp1 = vincenty(last, this)
        #print temp1
        temp1=get_distance(last[1],last[0],this[1],this[0])
        #print temp3
        
        #abs(a - b)<epsilon
        if abs(temp1-0) > epsilon:
            SUM += temp1
        else:
           # temp2 = vincenty(prelast, this)
            temp2=get_distance(prelast[1],prelast[0],this[1],this[0])
            if abs(temp2-0) > epsilon:
                SUM += temp2
                 
            else:
                SUM += 10
        #print(last)
        dis.append(SUM) 
        last = this
        prelast = last
        
    return dis

###############################################################################
###############################################################################

