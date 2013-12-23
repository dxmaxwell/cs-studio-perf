#!/usr/bin/python2

import sys, csv

from datetime import datetime

if len(sys.argv) > 1:
    try:
        tracerDataFile = open(sys.argv[1], "r")
    except:
        print "Error while openning: ", sys.argv[1]
        sys.exit(1)
else:
    tracerDataFile = sys.stdin

tracerReader = csv.reader(tracerDataFile)
tracerWriter = csv.writer(sys.stdout)

# write the header
header = tracerReader.next()
tracerWriter.writerow(header)

tracerDateFormat = "%I:%M:%S.%f %p, %b %d, %Y"

initial = 0

for row in tracerReader:
    if initial == 0:
        initial = datetime.strptime(row[0], tracerDateFormat)

    row[0] = (datetime.strptime(row[0], tracerDateFormat) - initial).total_seconds();
    row[1] = row[1].replace(',','')
    row[2] = row[2].replace(',','')

    tracerWriter.writerow(row)
