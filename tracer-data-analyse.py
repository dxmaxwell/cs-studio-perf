#!/usr/bin/python2

import sys, csv, numpy

from datetime import datetime, timedelta
import matplotlib.pyplot as plt

if len(sys.argv) > 1:
    try:
        tracerDataFile = open(sys.argv[1], "r")
    except:
        print "Error while openning: ", sys.argv[1]
        sys.exit(1)
else:
    tracerDataFile = sys.stdin

tracerReader = csv.reader(tracerDataFile)

xcol = -1
ucol = -1
ccol = -1

# Figure out the column content using the header.
header = tracerReader.next()

for idx in range(len(header)):
    if header[idx] == "Time [ms]":
        xcol = idx
    elif header[idx] == "Used [B]":
        ucol = idx
    elif header[idx] == "CPU usage [%]":
        ccol = idx

if xcol < 0:
    print "Time data column not found"
    sys.exit(1)

if ucol < 0:
    print "Memory usage column not found"
    sys.exit(1)

if ccol < 0:
    print "CPU usage column not found"


tracerDateFormat = "%I:%M:%S.%f %p, %b %d, %Y"

initial = 0

# All the data goes into these arrays.
xdata = []
udata = []
cdata = []


# Minimuns go into these arrays.
xpoints = []
upoints = []

for row in tracerReader:
    if initial == 0:
        initial = datetime.strptime(row[xcol], tracerDateFormat)

    x = (datetime.strptime(row[xcol], tracerDateFormat) - initial).total_seconds()
    u = float(row[ucol].replace(',',''))
    c = float(row[ccol])

    if len(xdata) == 0:
        pass
    elif u < ulast and ulast-u > ulast*0.1:
        xpoints.append(x)
        upoints.append(u)

    xdata.append(x)
    udata.append(u)
    cdata.append(c)

    ulast = u

results =  numpy.polyfit(xdata, cdata, 1)
print "CPU Results"
print "\tNumber of Points:", len(cdata)
print "\tTotal Time Elapsed:", timedelta(seconds=xdata[len(xdata)-1])
print "\tLinear Fit Mean: %.2f%%" % (results[1],)
print

results =  numpy.polyfit(xdata, udata, 1)
print "Memory Results (All Data)"
print "\tNumber of Points:", len(xdata)
print "\tTotal Time Elapsed:", timedelta(seconds=xdata[len(xdata)-1])
print "\tLinear Fit Slope: %.2fB/s  (%.2fMB/h [MB=1048576B])" % (results[0], results[0]*3600/(1048576))
print

results = numpy.polyfit(xpoints, upoints, 1)
print "Memory Results (Minimums Only)"
print "\tNumber of Points:", len(xpoints)
print "\tTotal Time Elapsed:", timedelta(seconds=xpoints[len(xpoints)-1])
print "\tLinear Fit Slope: %.2fB/s  (%.2fMB/h [MB=1048576B])" % (results[0], results[0]*3600/(1048576))
print


#plt.plot(xdata, udata)
plt.plot(xpoints, upoints)
#plt.plot(xdata, cdata)
plt.show()
