###########################################################################
## V1 Scripts disks_LogCleaner
## last update 2018.11.2 01:#3
## purpose : UPDATE with date and time conversion!
## LuckyDucky + thelamehacker
###########################################################################

import pandas as pd
import numpy as np  
import csv
import datetime 
import dateutil
import re 

logPath= str('disks.log')
f=open(logPath,'r')
f2 = open('_disks.log', 'w')

f_clean = "-" * 80 + "\n"
f_clean2= "\n"

for line in f:
    if f_clean == line or f_clean2 ==line: 
        pass
    else:
        f2.write(line)    
f.close()
f2.close()

f2=open('_disks.log','r')
lines=f2.readlines()
#print(lines)    
f2.close()
holder=type(lines)
print(holder)
#elements in lines
print(len(lines)) 

f=open(logPath,'r')
f2=open('_disks.log','w')
strD=str(lines)
strD=''.join(lines)
strD=strD.replace(" 2018\n","")
strD=strD.replace("Sun Oct 28","2018-10-28")
strD=strD.replace("Device               Total     Used     Free  Use %      Type  Mount","")
f2.write(strD)
f.close()
f2.close()

f2=open('_disks.log','r')
lines2=f2.readlines()
#print(lines2)
#display number of element in lines2
print(len(lines2)) 

systemdata1=[lines2[0],lines2[1],lines2[2],lines2[3]]
systemdata2=[lines2[4],lines2[5],lines2[6],lines2[7],lines2[8]]
systemdata3=[lines2[9],lines2[10],lines2[11],lines2[12],lines2[13]]
systemdata4=[lines2[14],lines2[15],lines2[16],lines2[17]]
systemdata5=[lines2[18],lines2[19],lines2[20],lines2[21]]
systemdata6=[lines2[22],lines2[23],lines2[24],lines2[25]]
systemdata7=[lines2[26],lines2[27],lines2[28],lines2[29],lines2[30]]
systemdata8=[lines2[36],lines2[37],lines2[38],lines2[39],lines2[40]]
systemdata9=[lines2[41],lines2[42],lines2[43],lines2[44],lines2[45]]
systemdata10=[lines2[46],lines2[47],lines2[48],lines2[49],lines2[50]]
allsystemdata=[systemdata1,systemdata2,systemdata3,systemdata4,systemdata5,systemdata6,systemdata7,systemdata8,systemdata9,systemdata10]

print(systemdata1)

