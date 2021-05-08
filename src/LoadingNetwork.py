import Graph_Traversal
import math
import plot
import os
import base64
from multiprocessing import Pool
import gc
from tornado.websocket import WebSocketHandler
rawdata = open('NetworkWithDistance.txt')

with open('NetworkWithDistance.txt') as f:

    rawdata = f.readlines()

# you may also want to remove whitespace characters like `\n` at the end

# of each line

rawdata = [x.strip() for x in rawdata]
## TEXT ###############################################################################################################
class EchoWebSocket(WebSocketHandler):
    def open(self):
        print("WebSocket opened")

    def on_message(self, message):
        #self.write_message(u"You said: " + message)


#    def main(startlatlong, endlatlong, startdate, enddate,rawdata ):
        m=message[1:-1].split("&")
        
        startlatlong = [m[7].split("=")[1],m[8].split("=")[1]]

        endlatlong= [m[9].split("=")[1],m[10].split("=")[1]]


        startdate = m[11].split("=")[1]

        enddate = m[12].split("=")[1]
        print(startlatlong, endlatlong, startdate, enddate)


           


        Data = {}
        Adja = {}
        k = []
        Order = {}

    #"ID"   "Name"  "ToCell"    "FromCell"  "Order" "BasinID"   "BasinCells"    "Travel"    "CellArea"  "CellLength"    "SubbasinArea"  "SubbasinLength"    "CellXCoord"    "CellYCoord"    "DistToMouth"   "DistToOcean"
        flag = True
    #print 'check1'
    #dir = os.path.dirname(__file__)
    #filename = os.path.join(dir, 'NetworkWithDistance.txt')
    #with open('NetworkWithDistance.txt') as rawdata :
        i=0

        self.write_message("~0")
        for line in rawdata:
            i+=1

            if(i<=50):
                self.write_message("~"+str(i*1.0/100))
            if(flag):
                flag = False
            else:
                a = line.split()
                temp = [int(math.floor((float(a[12])+138)/0.05)),int(math.floor((float(a[13])-5)/0.05))]
                Data[(temp[0], temp[1])] = [False, 0 , 0, int(a[4])]

                adjalist = []
                d = 1
                X = a[2]
                val = [[d,0],[d,-d],[0, -d],[-d,-d],[-d,0],[-d,d],[0,d],[d,d]]
                for k in range(1,9):
                    if(int(a[2]) & (1<<(k-1))):
                        adjalist.append([temp[0]+val[k-1][0], temp[1]+val[k-1][1]])

                Adja[(int(math.floor((float(a[12])+138)/0.05)),int(math.floor((float(a[13])-5)/0.05)))] = adjalist
                
                
    #print 'check2'
    #######################################################################################################################
        start = int(math.floor((float(startlatlong[1])+138)/0.05)), int(math.floor((float(startlatlong[0])-5)/0.05))
        self.write_message("~0.55")
        goal  = int(math.floor((float(endlatlong[1])+138)/0.05)), int(math.floor((float(endlatlong[0])-5)/0.05))
        self.write_message("~0.60")
        if Graph_Traversal.bfs_shortest_path(Data, Adja, start, goal):
            res = Graph_Traversal.get_path(Data,start, goal)
            path = res[0]
            order = res[1]

       ## from multiprocessing import Pool
            pool = Pool(processes=3)
            a = pool.apply_async(Graph_Traversal.mean_discharge, [path,startdate, enddate])
            b = pool.apply_async(Graph_Traversal.mean_temperature, [path,startdate, enddate])
            c = pool.apply_async(Graph_Traversal.dis_in_km, [path])

            pool.close()
            pool.join()
            mean_temp = a.get()
        #
       #except:
          #return "Try with other points!!"
            mean_dis =  b.get()
            distance = c.get()
            self.write_message("~0.65")
            pool2 = Pool(processes=2)
            d = pool2.apply_async(Graph_Traversal.find_pwp, [path,distance])
       # e = pool2.apply_async(Graph_Traversal.major_trib, [order,distance])

            pool2.close()
            pool2.join()
        

            pwp_in_path = d.get()
            self.write_message("~0.70")
        #try:
        #  major_trib =  e.get()
       # except:
         # return "Try with other points!!"
        ##print 'step1', startdate,enddate,path,distance,mean_dis, mean_temp,pwp_in_path,major_trib
            Adja.clear()
            gc.collect()
            self.write_message("~0.90")
            
            ################
              #          output, str1, str2, str3 = LoadingNetwork.main(

          #      [start1, start2], [goal1, goal2], fromdate, todate, rawdata)

            #print str1,str2,str3

         #   after = time.time()

       #     print ("time,", after - before)



      #      if(isinstance(output, str)):


          #      return output, 201

         #   else:

              # gc.collect()

              #print base64.b64encode(output.getvalue())

           #     return base64.b64encode(

           #         output.getvalue()) + "***" + str1 + "***" + str2 + "***" + str3, 200
            ##############
            
            output, str1, str2, str3=plot.main(startdate,enddate,path,distance,mean_dis, mean_temp,pwp_in_path)#,major_trib)
            ae=base64.b64encode( output.getvalue())

            self.write_message( ae+ "***" + str1 + "***" + str2 + "***" + str3)

        else :
            gc.collect()
            self.write_message("~0.90")
            self.write_message("$")
            

    def on_close(self):
        print("WebSocket closed")
