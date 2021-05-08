from flask import Flask, request, render_template, send_file, Response

import io

import base64

import csv

import json

import time

from collections import OrderedDict

import numpy

import pandas as pd

from numpy import genfromtxt

from flask import jsonify

from flask_cors import CORS

from LoadingNetwork import EchoWebSocket

import shutil

import gc

from tornado.wsgi import WSGIContainer

from tornado.web import Application, FallbackHandler

from tornado.websocket import WebSocketHandler

from tornado.ioloop import IOLoop



app = Flask('flasknado')

#app = Flask(__name__)

app.debug = True

CORS(app)





##initial netwrok csv data############################

rawdata = open('NetworkWithDistance.txt')

with open('NetworkWithDistance.txt') as f:

    rawdata = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end

# of each line

rawdata = [x.strip() for x in rawdata]

my_data = genfromtxt('networkwithdist.csv', delimiter=',')

# my_data=numpy.delete(my_data,(0),axis=0)

header = ['id', 'id_to', 'lon', 'lat', 'basinid']

frame = pd.DataFrame(my_data, columns=header)

data = []

MY_GLOBAL = []

with open('tempcsv.csv') as f:

    for line in f:

        temp = line.strip().split(',')

        data.append(temp)

#############################

data1 = []

with open('MyFile1.txt') as f:

    r = 0

    for line in f:

        if(r > 0):

            data2 = []

        # print(line)

            temp = line.split("\",")

            data2.append(temp[0][1:])

            temp1 = temp[1].split(",[")

            data2.append(temp1[0])

            data2.append(temp1[1][:-2])

            data1.append(data2)

        r += 1

header = ['celllist', 'cellid', 'cellto']

frame_celllist = pd.DataFrame(data1, columns=header)

frame_celllist = frame_celllist.drop_duplicates()

del data1[:]

##################

data_c = []

with open('powerplant_cell_loc.csv') as f:

    r = 0

    for line in f:

        if(r > 0):



            data_cc = line.split(",")

            data_c.append(data_cc)



        # print(line)

        r += 1

header = ['cellid', 'loc']

frame_cell = pd.DataFrame(data_c, columns=header)

frame_cell = frame_cell.drop_duplicates()

del data_c[:]



########################################################

import os

import sys

from SimpleHTTPServer import SimpleHTTPRequestHandler

import BaseHTTPServer



# class MyHTTPRequestHandler(SimpleHTTPRequestHandler):

# def translate_path(self,path):

#    path = SimpleHTTPRequestHandler.translate_path(self,path)

#    if os.path.isdir(path):

#       for base in "index", "default":

#            for ext in ".html", ".htm", ".txt":

#              index = path + "/" + base + ext

#              if os.path.exists(index):

#               return index

#   return path



# def test(HandlerClass = MyHTTPRequestHandler,

#       ServerClass = BaseHTTPServer.HTTPServer):

#  BaseHTTPServer.test(HandlerClass, ServerClass)





##################travesal network upstream############

'''def find_upstream(value):

   gc.collect()

   ii=0

   li = []

   temp=[]

   a=frame.ix[int(value)]

   temp.append(a)

   #print(MY_GLOBAL)

   MY_GLOBAL[:]=[]

   #x=data[int(value)]



   #x=frame[frame['id']==a['id_to']]

    #print x



   i=0

   z=0

   zz=0

   while zz<len(temp):



       item=temp[zz]

       zz+=1

       ##print(z,len(temp))

      ## item=temp.pop()

   ## print item

       #x=frame[frame['id_to']==item['id']]

       x=data[int(float(item['id']))]

    #print x



       i=1



       while i<len(x) :

       #   d = OrderedDict()

        #  xx=x.loc[x.index[i]]

          xx=frame.ix[int(float(x[i]))]

       #   d['type'] = 'Feature'

       #   d['geometry'] = {

       #     'type': 'MultiLineString',

       #     'coordinates': [[[float(xx['lon']),float(xx['lat'])],[float(item['lon']), float(item['lat'])]]]

     #      }

     #     d['properties'] = { "id":int(xx['id']),"id_to":int(xx['id_to']),"lon": float(xx['lon']),"lat": float(xx['lat'])

         #  }

       #   li.append(d)

          i+=1

       #   ii+=1

          ##if ii%1000==0:

        ##  print ii

          temp.append(xx)

   print(len(temp))

   while z<len(temp):



       item=temp[z]

       z+=1

       ##print(z,len(temp))

      ## item=temp.pop()

   ## print item

       #x=frame[frame['id_to']==item['id']]

       x=data[int(float(item['id']))]

    #print x



       i=1



       while i<len(x) :

          d = OrderedDict()

          #xx=x.loc[x.index[i]]

          xx=frame.ix[int(float(x[i]))]

          d['type'] = 'Feature'

          d['geometry'] = {

            'type': 'MultiLineString',

            'coordinates': [[[float(xx['lon']),float(xx['lat'])],[float(item['lon']), float(item['lat'])]]]

           }

          d['properties'] = { "id":int(xx['id']),"id_to":int(xx['id_to']),"lon": float(xx['lon']),"lat": float(xx['lat'])

           }

          li.append(d)

          d = OrderedDict()

          #xx=x.loc[x.index[i]]

         # xx=frame.ix[int(float(x[i]))]



          i+=1

          ii+=1

          if ii%1000==0 or (ii+1)/len(temp)==1:



             MY_GLOBAL.append((int)((ii+1)/(len(temp)* 1.0)*100))

            ## print(checkInt,ii,len(temp))

        ##  print ii

         # temp.append(xx)

   #d = OrderedDict()

   #d['type'] = 'FeatureCollection'

   #d['features'] = li

   #print li

   print(ii)

   return li,200'''





def find_upstream(value):

    gc.collect()

    ii = 0

    li = []

    temp = []

    a = frame.ix[int(value)]

    temp.append(int(value))



    MY_GLOBAL[:] = []





    i = 0

    z = 0

    zz = 0



    jstring = ''

    while z < len(temp):



        item = frame.ix[temp[z]]

        z += 1



        x = data[int(float(item['id']))]

    #print x



        i = 1



        while i < len(x):





            xx = frame.ix[int(float(x[i]))]

            jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(float(xx['lon'])) + ',' + str(float(xx['lat'])) + '],[' + str(float(item['lon'])) + ',' + str(

                float(item['lat'])) + ']]]},"properties": {"id_to": ' + str(int(xx['id_to'])) + ',"id":' + str(int(xx['id'])) + ',"lat":' + str(float(xx['lat'])) + ',"lon": ' + str(float(xx['lon'])) + '}},'







            ii += 1

            temp.append(int(float(x[i])))

            i += 1

            if ii % 1000 == 0:

                # print(ii)

                MY_GLOBAL.append((int)((ii + 1) / (200000 * 1.0) * 100))

            # print(checkInt,ii,len(temp))

        ##  print ii

         # temp.append(xx)

    #d = OrderedDict()

    #d['type'] = 'FeatureCollection'

    #d['features'] = li

    #print li

#   print(jstring)

    MY_GLOBAL.append(100)

    return jstring[:-1], 200



##################travesal network downstream############





def find_downstream(value, sourceid):

    #print value,sourceid

    ii = 0

    li = []

    temp = []

    jstring = ''

    # MY_GLOBAL[:]=[]

    a = frame.ix[int(value)]

    temp.append(a)

    check = True

    z = 0

    while z < len(temp) and check:

        item = temp[z]

        z += 1

        if(item['id_to'] == sourceid):

            check = False

            # break

    ## print item

      # if(item['id']==sourceid):

        #  check=False

        x = frame.ix[frame['id'] == item['id_to']]

    #print x



        i = 0

        while i < len(x):

            #  d = OrderedDict()

            xx = x.ix[x.index[i]]

            jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(float(xx['lon'])) + ',' + str(float(xx['lat'])) + '],[' + str(float(item['lon'])) + ',' + str(

                float(item['lat'])) + ']]]},"properties": {"id_to": ' + str(int(xx['id_to'])) + ',"id":' + str(int(xx['id'])) + ',"lat":' + str(float(xx['lat'])) + ',"lon": ' + str(float(xx['lon'])) + '}},'



        #  d['type'] = 'Feature'

        #  d['geometry'] = {

         #   'type': 'MultiLineString',

         #   'coordinates': [[[float(xx['lon']),float(xx['lat'])],[float(item['lon']), float(item['lat'])]]]

         #  }

         # d['properties'] = { "id":int(xx['id']),"id_to":int(xx['id_to']),"lon": float(xx['lon']),"lat": float(xx['lat'])

         # }

         # li.append(d)

        #  d=OrderedDict()

            i += 1

            ii += 1



            temp.append(xx)

    #   if(item['id']==sourceid):

     #      check=False

    # MY_GLOBAL.append(100)



    # d = OrderedDict()

    # d['type'] = 'FeatureCollection'

    # d['features'] = li

    # print li

    # if (check==False):

    return jstring[:-1], 200





##################travesal network downstream############

def find_downstream1(value):

    #print value,sourceid

    ii = 0

    li = []

    temp = []

    jstring = ''

    # MY_GLOBAL[:]=[]

    a = frame.ix[int(value)]

    temp.append(a)

    check = True

    z = 0

    while z < len(temp) and check:

        item = temp[z]

        z += 1



    ## print item

      # if(item['id']==sourceid):

        #  check=False

        x = frame.ix[frame['id'] == item['id_to']]

    #print x



        i = 0

        while i < len(x):

            #  d = OrderedDict()

            xx = x.ix[x.index[i]]

            jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(float(xx['lon'])) + ',' + str(float(xx['lat'])) + '],[' + str(float(item['lon'])) + ',' + str(

                float(item['lat'])) + ']]]},"properties": {"id_to": ' + str(int(xx['id_to'])) + ',"id":' + str(int(xx['id'])) + ',"lat":' + str(float(xx['lat'])) + ',"lon": ' + str(float(xx['lon'])) + '}},'



        #  d['type'] = 'Feature'

        #  d['geometry'] = {

         #   'type': 'MultiLineString',

         #   'coordinates': [[[float(xx['lon']),float(xx['lat'])],[float(item['lon']), float(item['lat'])]]]

         #  }

         # d['properties'] = { "id":int(xx['id']),"id_to":int(xx['id_to']),"lon": float(xx['lon']),"lat": float(xx['lat'])

         # }

         # li.append(d)

        #  d=OrderedDict()

            i += 1

            ii += 1



            temp.append(xx)

    #   if(item['id']==sourceid):

     #      check=False

    # MY_GLOBAL.append(100)



    # d = OrderedDict()

    # d['type'] = 'FeatureCollection'

    # d['features'] = li

    # print li

    # if (check==False):

    return jstring[:-1], 200

#######################pp upstream#######################





def find_upstream_pp(cellid):

    gc.collect()

# header=['celllist','cellid','cellto']

# header=['cellid','loc']



    templi = frame_celllist[frame_celllist['cellid']

                            == cellid]['celllist'].tolist()



    templist = templi[0][1:-1].split(",")



    z = 0

    jstring = ''

    while z < len(templist):



        curid = templist[z].strip()

    # print(curid,templist)

        curidloc = frame_cell[frame_cell['cellid'] == curid]['loc'].tolist()

        curidloc1 = curidloc[0].split("_")

        # print(curidloc1[0],curidloc1[1][:-1],curidloc[0])

        z += 1

        temp = frame_celllist[frame_celllist['cellid']

                              == curid]['cellto'].tolist()

        print(temp)

        temp = temp[0].split(",")



        if len(temp) == 1 and temp[0][:-1] == "none":

         # print(temp[0])

            continue

        else:

            zz = 0

            while zz < len(temp):

                # print(temp[zz],temp)

                x = temp[zz]

                zz += 1

                if zz == len(temp):

                    nextloc = frame_cell[frame_cell['cellid']

                                         == x[:-1]]['loc'].tolist()

                else:

                    nextloc = frame_cell[frame_cell['cellid']

                                         == x]['loc'].tolist()



                nextloc1 = nextloc[0].split("_")



        # print(nextloc1[0],nextloc1[1][:-1],nextloc1)

                jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(curidloc1[0]) + ',' + str(curidloc1[1][:-1]) + '],[' + str(

                    nextloc1[0]) + ',' + str(nextloc1[1][:-1]) + ']]]},"properties": {"lat":' + str(curidloc1[1][:-1]) + ',"lon": ' + str(curidloc1[0]) + '}},'

        #  jstring+='{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[['+str(float(xx['lon']))+','+str(float(xx['lat']))+'],['+str(float(item['lon']))+','+str(float(item['lat']))+']]]},"properties": {"id_to": '+str(int(xx['id_to']))+',"id":'+str(int(xx['id']))+',"lat":'+str(float(xx['lat']))+',"lon": '+str(float(xx['lon']))+'}},';



    return jstring[:-1], 200

#######################pp downstream#######################





def find_downstream_pp(cellid, dcellid):

    gc.collect()

# header=['celllist','cellid','cellto']

# header=['cellid','loc']

    print(cellid, dcellid)

    templi = frame_celllist[frame_celllist['cellid']

                            == cellid]['celllist'].tolist()



    templist = templi[0][1:-1].split(",")



    z = len(templist) - 1

    jstring = ''

    while z > 0:

        print(templist[z].strip())

        curid = templist[z].strip()

        if curid != str(dcellid):

            z -= 1

        else:

            print(z)

            break



    while z > 0:

        curid = templist[z].strip()

    # print(curid,templist)

        curidloc = frame_cell[frame_cell['cellid'] == curid]['loc'].tolist()

        curidloc1 = curidloc[0].split("_")

        # print(curidloc1[0],curidloc1[1][:-1],curidloc[0])



        temp = frame_celllist[frame_celllist['cellid']

                              == templist[z].strip()]['cellto'].tolist()

        z -= 1

        print(temp)

        temp = temp[0].split(",")



        if len(temp) == 1 and temp[0][:-1] == "none":

         # print(temp[0])

            z -= 1

            continue

        else:

            zz = 0

            aaaa = 'false'

            while zz < len(temp):

                # print(temp[zz],temp)

                x = temp[zz]

                zz += 1

                if zz == len(temp):

                    if x[:-1] == curid:

                        aaaa = 'true'

                        nextloc = frame_cell[frame_cell['cellid']

                                             == x[:-1]]['loc'].tolist()

                else:

                    if x == curid:

                        aaaa = 'true'

                        nextloc = frame_cell[frame_cell['cellid']

                                             == x]['loc'].tolist()

                if aaaa == 'true':

                    nextloc1 = nextloc[0].split("_")



        # print(nextloc1[0],nextloc1[1][:-1],nextloc1)

                    jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(curidloc1[0]) + ',' + str(curidloc1[1][:-1]) + '],[' + str(

                        nextloc1[0]) + ',' + str(nextloc1[1][:-1]) + ']]]},"properties": {"lat":' + str(curidloc1[1][:-1]) + ',"lon": ' + str(curidloc1[0]) + '}},'

        #  jstring+='{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[['+str(float(xx['lon']))+','+str(float(xx['lat']))+'],['+str(float(item['lon']))+','+str(float(item['lat']))+']]]},"properties": {"id_to": '+str(int(xx['id_to']))+',"id":'+str(int(xx['id']))+',"lat":'+str(float(xx['lat']))+',"lon": '+str(float(xx['lon']))+'}},';

    print(jstring)

    if len(jstring) > 0:



        return jstring[:-1], 200

    else:

        return jstring, 200









@app.route("/", methods=['GET', 'POST'])

def index():

    print(request)

    return render_template('test1.html')





@app.route("/api/", methods=['GET', 'POST'])

def update():

    print(request.method)

    if request.method == "POST":



        source = request.form["source"]

        dist = request.form["dist"]

        pic = request.form["pic"]

        downfirst = request.form["downfirst"]



        pp = request.form["pp"]

        print(pp, source, dist, downfirst, pic)



        if(pp == 'yes'):

            upstream = request.form["upstream"]

            if(upstream == 'yes'):



                ucellid = request.form["ucellid"]

                re, ii = find_upstream_pp(ucellid)

        #  print(re)

                return json.dumps(re), ii



            #   if(upstream=='no'):



     ###     ucellid = request.form["ucellid"]

     #     dcellid = request.form["dcellid"]

     #     re,ii=find_downstream_pp(ucellid,dcellid)

            #    print(re)



    #     if(pp=='no'):

        source = request.form["source"]

        dist = request.form["dist"]

        pic = request.form["pic"]

        downfirst = request.form["downfirst"]



        #print dist

        if(downfirst == 'no'):

            if(source == 'yes'):

                sourceid = request.form["sourceid"]

                #print sourceid

                import time

                start = time. time()



                re, ii = find_upstream(sourceid)

                end = time. time()

                #print ii,(end-start)

                # print(re)

                # print(MY_GLOBAL)



                return json.dumps(re), ii



            if(dist == 'yes'):

                distid = request.form["distid"]

                sourceid = request.form["sourceid"]

                MY_GLOBAL[:] = []

#print distid,sourceid

                re, ii = find_downstream(int(distid), int(sourceid))

                print (re)

                gc.collect()

                MY_GLOBAL.append(100)

                return json.dumps(re, sort_keys=False, indent=4), ii

        if(downfirst == 'yes'):



            if(dist == 'yes'):

                distid = request.form["distid"]

                sourceid = request.form["sourceid"]

                MY_GLOBAL[:] = []

#print distid,sourceid

                re, ii = find_downstream1(int(distid))

                print (re)

                gc.collect()

                MY_GLOBAL.append(100)

                return json.dumps(re, sort_keys=False, indent=4), ii



        if(pic == 'yes'):

                        #print request.form

            MY_GLOBAL[:] = []

            start1 = request.form["dist_lat"]

            start2 = request.form["dist_lon"]

            goal1 = request.form["source_lat"]

            goal2 = request.form["source_lon"]

            fromdate = request.form["from"]

            todate = request.form["to"]


            import time

            before = time.time()

            output, str1, str2, str3 = LoadingNetwork.main(

                [start1, start2], [goal1, goal2], fromdate, todate, rawdata)

            #print str1,str2,str3

            after = time.time()

            print ("time,", after - before)



            if(isinstance(output, str)):


                return output, 201

            else:

              # gc.collect()

              #print base64.b64encode(output.getvalue())

                return base64.b64encode(

                    output.getvalue()) + "***" + str1 + "***" + str2 + "***" + str3, 200








class WebSocket(WebSocketHandler):





    def on_message(self, message):

     #   self.write_message("Received: " + message)

      #  self.write_message("Received2: " + message)

       # m=message.split("&")

        

        print("Received message: " + m[0])

        print("Received message: " + m[1])

        print("Received message: " + m[2])

        print("Received message: " + m[3])

        print("Received message: " + m[4])

        print("Received message: " + m[5])

        print("Received message: " + m[6])



        m=message[1:-1].split("&")

        

        source = m[0].split("=")[1]

        value = m[1].split("=")[1]

        dist = m[2].split("=")[1]

        value1 = m[3].split("=")[1]

        pic = m[4].split("=")[1]

        downfirst = m[5].split("=")[1]



        pp = m[6].split("=")

        print(pp, source, dist, downfirst, pic,value,value1)

###################################upstram##########################3

        if(downfirst == 'no'):

            if(source == 'yes'):


##################

                gc.collect()

                ii = 0

                li = []

                temp = []

                a = frame.ix[int(value)]

                temp.append(int(value))



                





                i = 0

                z = 0

                zz = 0



                jstring = ''

                

                while z < len(temp):



                     item = frame.ix[temp[z]]

                     z += 1



                     x = data[int(float(item['id']))]

    #print x

                     

                     i = 1



                     while i < len(x):





                         xx = frame.ix[int(float(x[i]))]

                         jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(float(xx['lon'])) + ',' + str(float(xx['lat'])) + '],[' + str(float(item['lon'])) + ',' + str(

                         float(item['lat'])) + ']]]},"properties": {"id_to": ' + str(int(xx['id_to'])) + ',"id":' + str(int(xx['id'])) + ',"lat":' + str(float(xx['lat'])) + ',"lon": ' + str(float(xx['lon'])) + '}},'







                         ii += 1

                         temp.append(int(float(x[i])))

                         i += 1

                     if(len(jstring)>1500000):

                         zz+=5

                         self.write_message( jstring[:-1])

                         self.write_message( '~'+str(zz*1.0/100))

                         jstring = ''

                     

                     

                self.write_message( jstring[:-1])

                self.write_message( '~1')

                

  



############################downstream#########################

            if(dist == 'yes'):



########################################################################

                 ii = 0

                 li = []

                 temp = []

                 jstring = ''

    # MY_GLOBAL[:]=[]

                 a = frame.ix[int(value1)]

                 temp.append(a)

                 check = True

                 z = 0

                 zz=0

                 while z < len(temp) and check:

                     item = temp[z]

                     z += 1

                     if(item['id_to'] == int(value)):

                         check = False


                     x = frame.ix[frame['id'] == item['id_to']]

    #print x



                     i = 0

                     while i < len(x):

            #  d = OrderedDict()

                         xx = x.ix[x.index[i]]

                         jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(float(xx['lon'])) + ',' + str(float(xx['lat'])) + '],[' + str(float(item['lon'])) + ',' + str(

                         float(item['lat'])) + ']]]},"properties": {"id_to": ' + str(int(xx['id_to'])) + ',"id":' + str(int(xx['id'])) + ',"lat":' + str(float(xx['lat'])) + ',"lon": ' + str(float(xx['lon'])) + '}},'




                         i += 1

                         ii += 1



                         temp.append(xx)


                     if(len(jstring)>150000):

                         zz+=5

                         self.write_message( jstring[:-1])

                         self.write_message( '~'+str(zz*1.0/100))

                         jstring = ''

                     

                     

                 self.write_message( jstring[:-1])

                 self.write_message( '~1')



##########################downfirst##############################################

        if(downfirst == 'yes'):

            if(dist == 'yes'):

                 ii = 0

                 li = []

                 temp = []

                 jstring = ''

    # MY_GLOBAL[:]=[]

                 a = frame.ix[int(value1)]

                 temp.append(a)



                 z = 0

                 zz=0

                 while z < len(temp) :

                     item = temp[z]

                     z += 1



            # break

    ## print item

      # if(item['id']==sourceid):

        #  check=False

                     x = frame.ix[frame['id'] == item['id_to']]

    #print x



                     i = 0

                     while i < len(x):

            #  d = OrderedDict()

                         xx = x.ix[x.index[i]]

                         jstring += '{"type": "Feature","geometry": { "type": "MultiLineString", "coordinates": [[[' + str(float(xx['lon'])) + ',' + str(float(xx['lat'])) + '],[' + str(float(item['lon'])) + ',' + str(

                         float(item['lat'])) + ']]]},"properties": {"id_to": ' + str(int(xx['id_to'])) + ',"id":' + str(int(xx['id'])) + ',"lat":' + str(float(xx['lat'])) + ',"lon": ' + str(float(xx['lon'])) + '}},'



        #  d['type'] = 'Feature'

        #  d['geometry'] = {

         #   'type': 'MultiLineString',

         #   'coordinates': [[[float(xx['lon']),float(xx['lat'])],[float(item['lon']), float(item['lat'])]]]

         #  }

         # d['properties'] = { "id":int(xx['id']),"id_to":int(xx['id_to']),"lon": float(xx['lon']),"lat": float(xx['lat'])

         # }

         # li.append(d)

        #  d=OrderedDict()

                         i += 1

                         ii += 1



                         temp.append(xx)

    #   if(item['id']==sourceid):

     #      check=False

    # MY_GLOBAL.append(100)



    # d = OrderedDict()

    # d['type'] = 'FeatureCollection'

    # d['features'] = li

    # print li

    # if (check==False):

                     if(len(jstring)>150000):

                         zz+=5

                         self.write_message( jstring[:-1])

                         self.write_message( '~'+str(zz*1.0/100))

                         jstring = ''


                 self.write_message( jstring[:-1])

                 self.write_message( '~1')
      # if(downfirst == 'yes'):
        if(pic == 'yes'):

                        #print request.form

   #"&dist_lat="+dist_lat+"&dist_lon="+dist_lon+"&source_lat="+source_lat+"&source_lon="+source_lon+"&from="+value3.value+"&to="+value4.value);         
#m[6].split("=")
      #      start1 = request.form["dist_lat"]

      #      start2 = request.form["dist_lon"]

      #      goal1 = request.form["source_lat"]

      #      goal2 = request.form["source_lon"]

    #        fromdate = request.form["from"]

       #     todate = request.form["to"]
            start1 = m[7].split("=")[1]

            start2 = m[8].split("=")[1]

            goal1 =m[9].split("=")[1]

            goal2 = m[10].split("=")[1]

            fromdate = m[11].split("=")[1]

            todate = m[12].split("=")[1] 
            print(start1,start2,goal1,goal2,fromdate,todate)


            import time

            before = time.time()

            output, str1, str2, str3 = LoadingNetwork.main(

                [start1, start2], [goal1, goal2], fromdate, todate, rawdata)

            #print str1,str2,str3
           # print(output)

            after = time.time()

            print ("time,", after - before)



        #    if(isinstance(output, str)):


         #       return output, 201

         #   else:

              # gc.collect()

              #print base64.b64encode(output.getvalue())

       #         return base64.b64encode(

            #        output.getvalue()) + "***" + str1 + "***" + str2 + "***" + str3, 200
#











if __name__ == "__main__":

    container = WSGIContainer(app)

    server = Application([

        (r'/websocket/', WebSocket),
              (r'/we/', EchoWebSocket),

        (r'.*', FallbackHandler, dict(fallback=container))

    ])

    server.listen(5000)

    IOLoop.instance().start()



    #  test()

