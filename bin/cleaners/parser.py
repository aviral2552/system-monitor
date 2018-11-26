import glob
import os

import machineTagger

from cleaners import *

logDir = ''
currentDir = ''
cleanersDir = ''
dataDir = ''
prefFile = str('preferences.cfg')
machineID = ''
logSubDir = []

# Fetch and store absolute path of cleaner and log directories
# And read machine ID from preferences file
def setEnvironment():

    # Saving the current working directory for later use during machine ID capturing
    global currentDir
    currentDir = os.getcwd()

    # Navigating into cleaners directory and capturing path
    global cleanersDir
    os.chdir('cleaners')
    cleanersDir = os.getcwd()

    # Navigating into logs directory and capturing path
    global logDir
    os.chdir('../../logs/')
    logDir = os.getcwd()

    # Generating machine ID unconditionally
    os.chdir(currentDir)
    machineTagger.generateMachineID()
    
    # Reading preferences file for machine ID
    userPreferences = []
    with open(prefFile) as preferences:
        for line in preferences:
            userPreferences.append((line.split('=')[1]).strip())

    # Capturing machine ID to pass to individual cleaner modules later
    global machineID
    machineID = userPreferences[2]

    # Navigating into data directory and capturing path
    global dataDir
    os.chdir('..')
    if not os.path.isdir('data'):
        os.system('mkdir data')
    os.chdir('data')
    dataDir = os.getcwd()


def crawl():

    global logSubDir
    os.chdir(logDir)

    # Listing all sub-directories for logs
    logSubDir = glob.glob('*', recursive = False)


    # Iterating through every sub-directory, finding all log files and running appropriate cleaner script
    for subDir in logSubDir:
        os.chdir(logDir)
        os.chdir(subDir)
        logFileList = []
        logFileList = glob.glob('*.log', recursive = False)
        
        # Placeholder print statements for executing the real scripts. #networkIntClean.py not yet included
        for logFile in logFileList:

            if logFile == 'battery.log':
                 print('Running batteryLog cleaner for date: ' + subDir)
                 batteryClean.initiator(dataDir, machineID, str(logDir + '/' + subDir))

            if logFile == 'bootTime.log':
                print('Running bootTime cleaner for date: ' + subDir)
                bootTimeClean.initiator(dataDir, machineID, str(logDir + '/' + subDir))

            if logFile == 'logTracker.log':
                print('Running logTrackercleaner for date: ' + subDir)
                logTrackerClean.initiator(dataDir, machineID, str(logDir + '/' + subDir))

            if logFile == 'processes.log':
                print('Running processes cleaner for date: ' + subDir)
                processesClean.initiator(dataDir, machineID, str(logDir + '/' + subDir))

            if logFile == 'networkInterfaces.log':
                print('Running network Interface cleaner for date: ' + subDir)
                networkIntClean.initiator(dataDir, machineID, str(logDir + '/' + subDir))


def main():
    setEnvironment()
    crawl()

if __name__ == '__main__':
    main()