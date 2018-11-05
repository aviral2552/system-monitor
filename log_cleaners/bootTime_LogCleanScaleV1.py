###########################################################################
## V1 of scaled bootTime_LogCleanScaleV1.py
## last update 2018.11.3 19:06
## prototype 
## notes: mini scale to be tested across all local bootTime.log with all dates
## resources: https://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list
## LuckyDucky + thelamehacker
##########################################################################
import pandas as pd
import numpy as np  
import csv
import time
from datetime import datetime #use datetime.striptime to parse strings into datetimes
from dateutil.parser import parse
import re ##to remove trailing n from dataFram

logPath= str('bootTime.log')
f=open(logPath,'r')
lines=f.readlines()
f.close()
#print(lines)
#bLogEle varies on number of instances
bLogEle=(len(lines))
print(lines[3])
print(bLogEle)
#print(type(lines))

#auto pull date from log -> remove time -> this should work across all logs -> test with new boot log
logDate_c=lines[3]
logDate=[]
logDateEle=(len(lines[3]))
#print(logDateEle)

f=open(logPath,'r')
f2=open('s_bootTime.log','w')

f_clean = "-" * 80 + "\n"
f_clean2= "\n"

for line in f:
    if f_clean == line or f_clean2 ==line: 
        pass
    else:
        f2.write(line)    
f.close()
f2.close()
print(type(line))

#auto pull time from logs
for char in logDate_c:
    a=logDate_c.replace(logDate_c[11:20],"")
    logDate.append(a)

logDate=logDate[0]   
print(logDate)

f2=open('s_bootTime.log','r')
lines2=f2.readlines() 
f2.close()
print(lines2)
lines2ele=(len(lines2))
print(lines2ele)

#removing what can be removed"globally"
#remove Thu - 2018 - change date to 2018-10-25 (keep time), excess text #exact copy and paste of spaces mostly
f=open(logPath,'r')
f2 = open('s_bootTime.log', 'w')
strB=str(lines2)
strB= ''.join(lines2)
strB=strB.replace("Current system boot time is: ","")
f2.write(strB)
f.close()
f2.close()
#for visual and reference
f2=open('s_bootTime.log','r')
lines3=f2.readlines() 
f2.close()
print(lines3)
#keep here for scaling
lines3ele=(len(lines3))
print(lines3ele)
#count number of events per log on date 
loginstances=(len(lines2))/2
print(loginstances)
print(range(lines3ele))
print(lines3ele)

#x=int() #https://stackoverflow.com/questions/17555218/python-how-to-sort-a-list-of-lists-by-the-fourth-element-in-each-list
loginstances=int(loginstances)
list_=lines3
list_.sort(key=lambda x: x[3]) #3 to indicate sort by every 2nd element, index 3
#print(list_)
loginstances=int(loginstances)
sysdatetime=list_[0:loginstances]
bootdatetime=list_[loginstances:lines2ele]
print(sysdatetime)
print(bootdatetime)
f=open(logPath,'r')
#f2=open('DataFrame_Battery.log','w') ##index length seems to be set automatically by number of rows in category one - date
#index=range(8)
columns=["System Date & Time","Boot Date & Time"]
values=[ ]
df2=pd.DataFrame()
df2["System Date & Time"] = sysdatetime
df2["Boot Date & Time"]=bootdatetime

#datetime test conversion
s=df2["System Date & Time"]
df2["System Date & Time"]=pd.to_datetime(s)

s2=df2["Boot Date & Time"]
df2["Boot Date & Time"]=pd.to_datetime(s2)

#clean \n from entire dataframe (via regex)
##df2
print(df2)

df2.to_csv('s_bootTime_clean.csv')


