###############################################################################
# Cleaner for: systemMon.py 0.3a 
# Name: bootClean.py
#
# Author: LuckyDucky (https://github.com/itsalways5am)
# 
# Updated: 11 November 2018
#
###############################################################################


import csv
import datetime
import re

import pandas as pd

f = open('bootTime.log','r')

captureTime = ['timeStamp']
osFamily = ['osFamily']
osRelease = ['osRelease']
osPlatform = ['osPlatform']
osDescription = ['osDescription']
bootTime = ['bootTime']

i = 10

for line in f:
  
        if str(line).startswith('<log>') == True:
                i = 1
                continue
        if str(line).startswith('</log>') == True:
                i = 7
                continue

        if i == 1:
                captureTime.append(line)
        elif i == 2:
                osFamily.append(line)
        elif i == 3:
                osRelease.append(line)
        elif i == 4:
                osPlatform.append(line)
        elif i == 5:
                osDescription.append(line)
        elif i == 6:
                bootTime.append(line)
        i += 1

f.close()

df = pd.DataFrame(list(zip(captureTime, osFamily, osRelease, osPlatform, osDescription, bootTime)))

stuffToIgnore = ['<captureTime>', '</captureTime>',
                '<osFamily>', '</osFamily>',
                '<osRelease>', '</osRelease>',
                '<osPlatform>', '</osPlatform>',
                '<osDescription>', '</osDescription>',
                '<bootTime>', '</bootTime>',
                '\n']

for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex = True)

# KeyValue error here!!!!!!
# Not needed right now, but will need to figure out what is wrong
#df['timeStamp'] = pd.to_datetime(df['timeStamp'])

df.to_csv('bootTime.csv', index = False, header = False)