#!/usr/bin/env python
import os
import time
import signal
import csv
import subprocess
from os import chdir

#######################################################################################
#                          Global Variable Definition                                 #
#######################################################################################

# A List of all pids running in a Server 
pidlist = []

# A List of Instances Name from processes ID
pnamelist = []


#######################################################################################
#                             Function Definition                                     #
#######################################################################################

def getPidList():
        # You can find Processes ID using Java.
        # Change the command of Next line to Find your own Instances, 'Svr' is a part of KOS Naming Conventions.  
        for line in os.popen("ps -ef | grep java | grep Svr | grep -v grep | cut -c-175"): 
                fields = line.split()
                pid = fields[1]
                pidlist.append(pid)
        return pidlist

def getPnameList():
        # Now you can get Instances Name from Process ID. 
        for line in os.popen("ps -ef | grep java | grep Svr | grep -v grep | cut -c-175"):
                fields = line.split()
                # Customize the field number according to your application server vendors.
                # Set number [8][2:] for JEUS, [9][2:] for Weblogic. 
                Svrname = fields[8][2:]
                pnamelist.append(Svrname)
        return pnamelist

def getJstat(pid,pname):
      Result = []
      filename = ""
      for i in range(len(pname)):
          # For Loop that Iterate over the retrieved Jstat Data per Instance.
          filename = "todayData_" + pname[i] + ".csv"
          command = "jstat -gcutil " + pid[i] + " > " + filename
          os.system(command)
          with open(filename) as myfile:
                 # Read the CSV file in skipping First Row.
                 jstatInfo = list(myfile)[-1] 
                 rowValues = jstatInfo.split()
                 # Append the Date Column.
                 rowValues.append(time.strftime('%Y%m%d',time.localtime(time.time())))
                 Result.append(rowValues)      
      return Result
    

#######################################################################################
#                                 Main Script                                         #
#######################################################################################

# Log Directory Path Setting
dirpath = '/home/wasadm/jstatLog'

# Check if directory exists  
if not(os.path.isdir(dirpath)):
 os.makedirs(os.path.join(dirpath))

pidlist = getPidList()
pnamelist = getPnameList()

chdir(dirpath)  # Change Directory
JstatData = getJstat(pidlist,pnamelist)

for i in range(len(pnamelist)):   
  # Get JSTAT History
  filename = "JstatMonData_" + pnamelist[i] + ".csv"
  with open(filename, 'a') as outfile:
        outFileWriter = csv.writer(outfile)
        outFileWriter.writerow(JstatData[i])
        # Monitoring Perm Memory Usage.
        values = JstatData[i]
        values = [float (j) for j in values] 
        if values[4] < 70:
          os.system("echo safe > ./mon_" + pnamelist[i]  + ".log")
        elif values[4] >= 70 and values[4] < 85:
          os.system("echo critical > ./mon_" + pnamelist[i]  + ".log")
        else:
          os.system("echo fatal > ./mon_" + pnamelist[i]  + ".log")


#---------------------------------The End of Script---------------------------------#

