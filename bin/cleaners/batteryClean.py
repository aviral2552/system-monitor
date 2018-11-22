###############################################################
## batteryclean.py for systemMon.py
## last updated 21.11.2018  12:11
## purpose : cleaner update with day of week extraction
## authors: luckyducky + lamehacker
################################################################

import csv
import os
import re
from datetime import datetime

import pandas as pd

machineID = ''
dataDir = ''

# for holding purposes manually entering machine ID from preferences (needs to be entered as a string)
LogID = []
captureTime = []
supported = []
detected = []
charge = []
remaining = []
status = []
plugged = []

# Add headers if the battery log data csv file is empty
def addHeaders():
    global LogID, captureTime, supported
    global detected, charge, remaining
    global status, plugged

    LogID.append('Log ID')
    captureTime.append('Log time')
    supported.append('Supported')
    detected.append('Detected')
    charge.append('Current charge')
    remaining.append('Remaining time')
    status.append('Status')
    plugged.append('Plugged')

#function to define structure of logID
def generateLogID(logCount):
    if logCount <= 9 and logCount >= 0:
        placeholder = '000'
    elif logCount <= 99 and logCount >= 10:
        placeholder = '00'
    elif logCount > 99:
        placeholder = '0'
    date = captureTime[0][13:23]
    LogID.append(machineID + '_' + str(date) + '[' + placeholder + str(logCount) + ']')

def initiator():

    i = 10
    logCount = 0

    a = os.getcwd()

    with open('battery.log') as batteryLog:
        for line in batteryLog:

            if line.startswith('<log>') == True:
                i = 1
                continue

            if line.startswith('</log>') == True:
                logCount += 1
                generateLogID(logCount)
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

    # creates dataframe using list(zip('name of lists to be zipped into dataFrame'))
    df = pd.DataFrame(list(zip(LogID, captureTime, supported, detected, charge, remaining, status, plugged)))

    # defining items for regex to remove from dataframe
    stuffToIgnore = ['<captureTime>', '</captureTime>',
                    '<supported>', '</supported>',
                    '<detected>', '</detected>',
                    '<charge>', '</charge>',
                    '<status>', '</status>',
                    '<plugged>', '</plugged>',
                    '<remaining>', '</remaining>',
                    '\n']
    
    # regex for replacing stuff with ""
    for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex=True)

    os.chdir(dataDir)

    if os.path.exists('batteryLogs.csv') == True:
        with open('batteryLogs.csv', 'r') as batterLogs:
            temp_df = pd.read_csv('batteryLogs.csv')
            if temp_df.empty == False:
                addHeaders()

    with open('batteryLogs.csv', 'a') as batterLogs:
        df.to_csv(batterLogs, index=False, header=False)


def main(dd, mID):
    global dataDir, machineID
    
    dataDir = dd
    machineID = mID
    #os.chdir(lPath)

    initiator()

if __name__ == '__main__':

    # Starting with the default machine ID and log path if this script was run as standalone (not intended, but anyway)
    dd = '../../data/'
    mID = '00000000000000000000000000000000'
    #logPath = './'
    main(dd, mID)
