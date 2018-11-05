###########################################################################
## V1 of networkInterface_LogClean.py
## last update 2018.11.5 09:00
## local prototype 
## notes: 
## resources: 
## LuckyDucky 
###########################################################################

import pandas as pd
import numpy as np  
import csv
import time
from datetime import datetime #use datetime.striptime to parse strings into datetimes
from dateutil.parser import parse
import psutil
import re


logPath= str('networkInterfaces.log')
f=open(logPath,'r')
f2=open('_networkInterfaces.log', 'w')

#f_clean defines element we want to remove which is defined as line in f
#line is a string in f (lines defined later)
f_clean = "-" * 80 + "\n"
f_clean2= "\n"

for line in f:
    if f_clean == line or f_clean2 ==line: 
        pass
    else:
        f2.write(line)    
f.close()
f2.close()

f2=open('_networkInterfaces.log','r')
lines=f2.readlines()
print(lines[0])    
f2.close()
holder=type(lines)
print(len(lines))
#print(holder)

#global goal
logDate_=lines[0]
logDate=logDate_[0:10]
print(logDate)

netInt=[ ]
sysdatetime=[ ]
stats=[ ]
incoming=[ ]
outgoing=[ ]
mac=[ ]

for item in lines:
    item_s=str(item)
    if "    stats: " in item:
        stats.append(item)
    else:
        pass
    
    if "    incoming:" in item:
        incoming.append(item)
    else:
        pass
    
    if "    outgoing:" in item:
        outgoing.append(item)
    else:
        pass
    
    if "    MAC address   :" in item:
        mac.append(item)
    else:
        pass
    
    if logDate in item: 
        sysdatetime.append(item)
    else:
        pass

    if "    " in item or logDate in item:
        pass
    else:
        netInt.append(item)
            
#print(stats) 
#print(len(incoming))
#print(sysdatetime)
#print(netInt)
#print(len(netInt))

f=open(logPath,'r')
#index=range
values=[ ]
columns=["System Date & Time","NetInt","Stats","Incoming","Outgoing","MacAddress","IPV4:netmask","IPV6:netmask1","IPV6:netmask2","Other"]
df1=pd.DataFrame()
#df1["System Date & Time"]=sysdatetime
df1["NetInt"]=netInt
df1["Stats"]=stats
df1["Incoming"]=incoming    
df1["Outgoing"]=outgoing
#df1["MacAddress"]=mac
#df1["IPV4:netmask"]=netInt1IPv4         
#df1["IPV6:netmask1"]=netInt1IPv6a  
#df1["IPV6:netmask2"]=netInt1IPv6b
#df1["Other"]=[ ] 
#s=df1["System Date & Time"]
#df1["System Date & Time"]=pd.to_datetime(s)
df1=df1.replace('\n','',regex=True)
print(df1)

df1.to_csv('networkInterface_clean.csv')