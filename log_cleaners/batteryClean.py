###############################################################
## battery_clean.py for systemMon.py V0.3a
## last updated 11.11.2018 18:18
## authors: luckyducky and lamehacker
################################################################

import csv
import datetime
import re
import pandas as pd

f = open('battery.log','r')

captureTime = ['timeStamp']
supported = ['supported']
detected= ['detected']
charge = ['charge']
remaining = ['remaining']
status = ['status']
plugged = ['plugged']

i = 11

for line in f:
  
        if str(line).startswith('<log>') == True:
                i = 1
                continue
        if str(line).startswith('</log>') == True:
                i = 8
                continue
        if i == 1:
                captureTime.append(line)
        elif i == 2:
                supported.append(line)
        elif i == 3:
                detected.append(line)
        elif i == 4:
                charge.append(line)
        elif i == 5:
                remaining.append(line)
        elif i == 6:
                status.append(line)
        elif i == 7:
                plugged.append(line)        
        i += 1

df = pd.DataFrame(list(zip(captureTime, supported, detected, charge, remaining, status, plugged)))

stuffToIgnore = ['<captureTime>', '</captureTime>',
                '<supported>','</supported>',
                '<detected>', '</detected>',
                '<charge>', '</charge>',
                '<status>', '</status>',
                '<plugged>', '</plugged>',
                 '<remaining>','</remaining>',
                '\n']

for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex = True)
        
#df['timeStamp'] = pd.to_datetime(df['timeStamp'])

print(df)        
f.close()
df.to_csv('battery.csv')
