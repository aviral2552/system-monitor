###############################################################################
# Cleaner for: systemMon.py 0.3a
# Name: disksClean.py
#
# Author: LuckyDucky (https://github.com/itsalways5am) with lamehacker for
# steroid support (https://github.com/thelamehacker)
#
# Updated: 21 November 2018 12:25
###############################################################################

import pandas as pd
import csv
import re


# function to define structure of logID different than boot and battery
def format_logId_dsk():
    if log_count <= 9 and log_count >= 0:
        placeholder = '000'
    elif log_count <= 99 and log_count >= 10:
        placeholder = '00'
    elif log_count > 99:
        placeholder = '0'
    date = (timeStamp[13:23])
    uniqueLogId.append(machineID + str(date) + '[' + placeholder + str(log_count + 1) + ']')

def day():
    s = df[1]
    s2 = s[1:]
    df[1] = pd.to_datetime(s2)
    df['day'] = df[1].dt.dayofweek
    df.iloc[0, 1] = "timeStamp"
    df.iloc[0, 9] = "dayofweek"

machineID = '327d87e2c8870aed161afea1ef803dc4'
captureTime = ['timeStamp']
name = ['name']
size = ['size']
used = ['used']
free = ['free']
pctused = ['%used']
fileSys = ['fileSys']
mountPoint = ['mountPoint']
uniqueLogId = ['LogID']

log_count = 0  # For holding number of logs
timestampFix = 0
timeStamp = ''


with open('disks.log') as f:

    for line in f:
        if line.startswith('</log>') == True:
            log_count += 1 ##same as log_count=log_count+1

        if line.startswith('<captureTime>') == True:
            timeStamp = line
    # increase timestampFix by 1 each with each <name> ->to resolve the timestamp value != index length in dF
        if line.startswith('<name>') == True:
            name.append(line)
            captureTime.append(timeStamp)
            timestampFix += 1
            format_logId_dsk()

            # Used elif since only one of these conditions will be executed
            # for one iteration of the loop. Much faster execution
        elif line.startswith('<size>') == True:
            size.append(line)


        elif line.startswith('<used>') == True:
            used.append(line)

        elif line.startswith('<free>') == True:
            free.append(line)

        elif line.startswith('<%used>') == True:
            pctused.append(line)

        elif line.startswith('<fileSys>') == True:
            fileSys.append(line)

        elif line.startswith('<mountPoint>') == True:
            mountPoint.append(line)



df = pd.DataFrame(list(zip(uniqueLogId, captureTime, name, size, used, free, pctused, fileSys, mountPoint)))

stuffToIgnore = ['<captureTime>', '</captureTime>',
                 '<name>', '</name>',
                 '<size>', '</size>',
                 '<used>', '</used>',
                 '<free>', '</free>',
                 '<%used>', '</%used>',
                 '<fileSys>', '</fileSys>',
                 '<mountPoint>', '</mountPoint>',
                 '\n']

for stuff in stuffToIgnore:
    df = df.replace(stuff, "", regex=True)

day()

df.to_csv('disks.csv', index=True, header=False)

print(df)
