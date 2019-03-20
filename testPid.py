import os
import sys

#print(sys.version)

pidList = []
pnamelist = []

def getApachePid():
    for pid in os.popen("ps -ef | grep httpd | awk {'print $2'}"):
        field = pid.rstrip()
        pidList.append(field)

    return pidList

#print(getApachePid())


def getPnameList():
    # Now you can get Instances Name from Process ID.
    for line in os.popen("ps -ef | grep java | grep chul | grep -v grep | cut -c-175"):
        fields = line.split()
        # Customize the field number according to your application server vendors.
        # Set number [8][2:] for JEUS, [9][2:] for Weblogic.
        Svrname = fields[12][9:]
        pnamelist.append(Svrname)
    return pnamelist

#print(getPnameList())

#def makeCsvFile():
