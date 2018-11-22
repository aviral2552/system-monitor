###############################################################################
# Cleaner for: systemMon.py 0.3a 
# Name: logTrackerClean.py
#
# Author: LuckyDucky (https://github.com/itsalways5am) & lamehacker
# 
# Updated: 20 November 2018 13:31
###############################################################################

#import libraries needed to run script
import pandas as pd
import csv
import re


def format_logId():
    if log_count <= 9 and log_count >= 0:
        placeholder = '000'
    elif log_count <= 99 and log_count >= 10:
        placeholder = '00'
    elif log_count > 99:
        placeholder = '0'
    a = (captureTime[1])
    date = a[13:23]
    uniqueLogId.append(machineID + str(date) + '[' + placeholder + str(log_count) + ']')

def day():
    s = df[1]
    s2 = s[1:]
    df[1] = pd.to_datetime(s2)
    df['day'] = df[1].dt.dayofweek
    df.iloc[0, 1] = "timeStamp"
    df.iloc[0, 8] = "dayofweek"


machineID = '327d87e2c8870aed161afea1ef803dc4'
captureTime = ['timeStamp']
bootTime = ['bootTime']
processes= ['processes']
disks = ['disks']
networkInterfaces= ['networkInterfaces']
sensors = ['sensors']
battery= ['battery']
uniqueLogId=['LogID']

i = 12      #11 lines for each logTracker capture including log tags plus one n for empty line following
log_count = 0

with open('logTracker.log') as f:
    for line in f:
  
        if line.startswith('<log>') == True:
                i = 1
                continue
        if line.startswith('</log>') == True:
                log_count += 1
                format_logId()
                i = 11
                continue
        if i == 1:
                captureTime.append(line)
        elif i == 3:
                bootTime.append(line)
        elif i == 4:
                processes.append(line)
        elif i == 5:
                disks.append(line)
        elif i == 6:
                networkInterfaces.append(line)
        elif i == 7:
                sensors.append(line)
        elif i == 8:
                battery.append(line)        
        i += 1

f.close()
#creating dataframe (with no typecast chances) using zip() bring together lists 
df = pd.DataFrame(list(zip(uniqueLogId,captureTime, bootTime,processes,disks,networkInterfaces,sensors,battery)))

#creating list of strings for regex to strip prior to putting in dataFrame
stuffToIgnore = ['<captureTime>', '</captureTime>',
                '<bootTime>','</bootTime>','<processes>',
                '</processes>', '<disks>','<networkInterfaces>'
                '<sensors>','</sensors>','<battery>','</battery>','\n']

for stuff in stuffToIgnore:
    df = df.replace(stuff, "", regex = True)

day()
              
df.to_csv('logTracker.csv', index = False, header = False)

print(df)
