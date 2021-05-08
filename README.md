
[tool's link] test-visualization.environmentalcrossroads.net/plot/

*App dir: src dir

**Make sure you have datasets files: (EXP.)Discharge_dTS2017.nc,  qtx_watertemp_dTS2017.nc


** before run the python , please install following python's package: flask, flask-cors, vincent, matplotlib, numpy, pandas, seaborn, netCDF4 

Run flask firstly: 


$ export FLASK_APP=app.py(linux)
$ set FLASK_APP=app.py(windows powershell)

$ python -m flask run --host=0.0.0.0


Then open index.html locally 

If you want to access ip to show the map:

open a new terminal , run python server.py and see 0.0.0.0:8000 on the browser


Map:
![Alt text](/img1.png "Screenshot 1")
Large upstream:
![Alt text](/img2.png "Screenshot 1")
![Alt text](/img3.png "Screenshot 1")


![Alt text](/img4.png "Screenshot 1")
![Alt text](/img5.png "Screenshot 1")
![Alt text](/img6.png "Screenshot 1")

