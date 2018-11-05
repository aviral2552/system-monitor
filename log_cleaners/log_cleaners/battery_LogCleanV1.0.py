###########################################################################
## V1.0 of bootTime LogCleaner /bootTime_LogCleanerV3.py
## last update 2018.11.1 12:47
## prototype V1.0 -> clean and convert bootTime.log to .csv
## notes: specific solution, next step (mini scale)- one script for all bootTime.log
## LuckyDucky + thelamehacker
###########################################################################

import pandas as pd
import numpy as np  
import csv
import datetime #use datetime.striptime to parse strings into datetimes
import dateutil
import re ##to remove trailing n from dataFrame


logPath= str('battery.log')
f=open(logPath,'r')
f2 = open('_battery.log', 'w')
#placeholder for columns
#f2.write(columnname) 

#f_hoot defines element we want to remove which is defined as line in f
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

#f2 to refer to new file _battery.log
f2=open('_battery.log','r')
lines=f2.readlines()
#print(lines)    
f2.close()
#holder=type(lines)
#print(holder)

#using exact copy paste to remove #DT test - remove Tue, 2019 and change Oct 30 (2018) to "%Y-%m-%d %H:%M:%S"
#remove% to convert to float later so that python/pd understands
f=open(logPath,'r')
f2 = open('_battery.log', 'w')
#convert list to string 
strL=str(lines)
strL= ''.join(lines)
strL=strL.replace("Tue Oct 30","2018-10-30")
strL=strL.replace("Current charge:     ","")
strL=strL.replace("Status:     ","")
strL=strL.replace("Plugged in: ","")
strL=strL.replace("Left:       ","")
strL=strL.replace(" 2018","")
strL=strL.replace("%","")
#strL=strL.replace("Oct 30 ","")
#copy paste exact spaces in lines -i.e before strings [ ]
f2.write(strL)
f.close()
f2.close()
#for visual and reference
f2=open('_battery.log','r')
lines2=f2.readlines() 
f2.close()
#print(lines2)
#print(lines2[2])
#keep len line info for scaling info
#print(len(lines2)

#inserting missing values manually - learn how to do this auto, seems to work best here
#list.insert(i,x) ->location of insert and what you want to insert - here need to have Fully Charged to keep 
#missing value Charge Left when battery is full - represented here with24:60:60
lines2.insert(2,'24:60:60')
lines2.insert(7,'24:60:60')
#print(lines2)
#print(len(lines2)-1) #elements check for loops future etc. more automatic
#add range to date? #pattern of 5 - there must be a way to automate this
datetime=[lines2[0],lines2[5],lines2[10],lines2[15],lines2[20],lines2[25],lines2[30],lines2[35]]
currentcharge=[(lines2[1]),(lines2[6]),(lines2[11]),(lines2[16]),(lines2[21]),(lines2[26]),(lines2[31]),(lines2[36])] 
chargeleft=[lines2[2],(lines2[7]),(lines2[12]),(lines2[17]),(lines2[22]),(lines2[27]),(lines2[32]),(lines2[37])]
status=[lines2[3],lines2[8],lines2[13],lines2[18],lines2[23],lines2[28],lines2[33],lines2[38]]
pluggedin=[lines2[4],lines2[9],lines2[14],lines2[19],lines2[24],lines2[29],lines2[34],lines2[39]]
print(currentcharge)
#print(chargeleft)


#index is number of rows - can we autopopulate this? Maybe with some sort of row count 
f=open(logPath,'r')
#f2=open('DataFrame_Battery.log','w') ##index length seems to be set automatically by number of rows in category one - date
index=range(8)
columns=["System Date & Time","Current Charge%","Charge Left","Status","Plugged In"]
values=[ ]
df2=pd.DataFrame()
df2["System Date & Time"] =[lines2[0],lines2[5],lines2[10],lines2[15],lines2[20],lines2[25],lines2[30],lines2[35]]
df2["Current Charge"]=[float(lines2[1]),float(lines2[6]),float(lines2[11]),float(lines2[16]),float(lines2[21]),float(lines2[26]),float(lines2[31]),float(lines2[36])] 
df2["Charge Left"]=[lines2[2],lines2[7],lines2[12],lines2[17],lines2[22],lines2[27],lines2[32],lines2[37]]
df2["Status"]=[lines2[3],lines2[8],lines2[13],lines2[18],lines2[23],lines2[28],lines2[33],lines2[38]]
df2["Plugged In"] =[lines2[4],lines2[9],lines2[14],lines2[19],lines2[24],lines2[29],lines2[34],lines2[39]] 

#datetime test conversion
s=df2["System Date & Time"]
df2["System Date & Time"]=pd.to_datetime(s)

#clean \n from entire dataframe (via regex)
df2=df2.replace('\n','',regex=True)
df2

f.close()
f2.close()
#df2
print(df2)
df2.dtypes  #for informational purposes only (for conversions in this case)

#export to csv
df2.to_csv('battery_clean.csv')


