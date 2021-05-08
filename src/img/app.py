from flask import request
import LoadingNetwork
#from io import BytesIO
import base64
from flask import Flask, send_file
import io

#@app.route('/')
#def abc():
#	return "hello"
app = Flask(__name__)

@app.route('/', methods=['GET'])
def getQ():
    #/?startlat=39.925&startlong=-87.425&goallat=30.025&goallong=-90.475&from=2016-01-16&to=2018-04-19
    start1 = request.args.get('startlat')
    start2 = request.args.get('startlong')
    goal1  = request.args.get('goallat') 
    goal2  = request.args.get('goallong')
    fromdate = request.args.get('from')
    todate = request.args.get('to')
    #startdate = "2004-01-16"
    #enddate = "2004-04-19"
    #startlatlong = [39.925, -87.425]
    #endlatlong = [30.025, -90.475]
    import time
    before = time.time()
    output = LoadingNetwork.main([start1,start2], [goal1,goal2], fromdate, todate)
    after = time.time()
    print ("time,",after-before)
    if(type(output)==str):
        return output
    else:
        return send_file(
        #io.BytesIO(bites.read()),
        #io.BytesIO(bites.read()),
        output,
        attachment_filename='logo.png',
        mimetype='image/png'
        )
