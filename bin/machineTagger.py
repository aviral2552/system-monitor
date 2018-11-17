import hashlib
import os
import platform
import subprocess
import uuid

machineID = ''
pref = []
prefFile = str('preferences.cfg')

# Reading the preferences file and generating machine ID if the value is 0

def readPreferences():
   
    global machineID
    global pref

    with open(prefFile) as f:
        for line in f:
            pref.append((line.split('=')[1]).strip())
    
    if pref[2] == '0':
        generateMachineID()

# Identifying the operating system and calling appropriate function to generate the machine ID
def generateMachineID():
    
    mySys = platform.system()

    if mySys == 'Windows':
        generateForWindows()
    elif mySys == 'Darwin':
        generateForMacOS()
    elif mySys == 'Linux':
        generateForLinux()

# Generates machine ID for macOS based systems

def generateForMacOS():
    # first storage drive's serial number
    storageCMD = "/usr/sbin/diskutil info / | /usr/bin/awk '$0 ~ /UUID/ { print $3 }'"
    sysStorage,error = subprocess.Popen(storageCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sysStorage = sysStorage.decode().split('\n')[0].strip()

    # system's serial number
    uuidCMD = "system_profiler SPHardwareDataType | grep -i 'Serial Number (system):' | awk '{print $4}'"
    sysUUID,error = subprocess.Popen(uuidCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sysUUID = sysUUID.decode().split('\n')[0].strip()

    # system's hardware address as a 48-bit positive integer
    sysMACAddr = uuid.getnode()

    # create a new sha3_512 object
    machineHash = hashlib.sha3_512()
    # encode as utf-8 and add storage serial number, system UUID and MAC address and hash it
    machineHash.update(str(sysStorage).encode('utf-8') + str(sysUUID).encode('utf-8') + str(sysMACAddr).encode('utf-8'))

    # truncate and store the hexdigest as machineID
    global machineID
    machineID = machineHash.hexdigest()[0:10]
    writeMachineID(machineID)

# Generates machine ID for Windows based systems

def generateForWindows():
    # first storage drive's serial number
    sysStorage = subprocess.check_output('wmic DISKDRIVE get SerialNumber').decode().split('\n')[1].strip()

    # system's UUID
    sysUUID = subprocess.check_output('wmic csproduct get UUID').decode().split('\n')[1].strip()

    # system's hardware address as a 48-bit positive integer
    sysMACAddr = uuid.getnode()

    # create a new sha3_512 object
    machineHash = hashlib.sha3_512()
    # encode as utf-8 and add storage serial number, system UUID and MAC address and hash it
    machineHash.update(str(sysStorage).encode('utf-8') + str(sysUUID).encode('utf-8') + str(sysMACAddr).encode('utf-8'))

    # truncate and store the hexdigest as machineID
    global machineID
    machineID = machineHash.hexdigest()[0:10]
    writeMachineID(machineID)

# Generates machine ID for Linux based systems

def generateForLinux():
    print('Placeholder')

# Writes the new machine ID to the preferences file

def writeMachineID(newID):

    f = open(prefFile, 'w')
    f.write('numberOfLogs=' + str(pref[0]) + '\ncollectionFrequency=' + str(pref[1]) + '\nmachineID=' + str(newID))
    f.close()

if __name__ == '__main__':
    readPreferences()
