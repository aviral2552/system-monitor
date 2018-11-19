import hashlib
import os
import platform
import subprocess
import uuid

# Global variables to hold reused values across the program
machineID = ''
pref = []
prefFile = str('preferences.cfg')

# Reading the preferences file and writing machineID if it looks different
def readPreferences():
   
    global machineID
    global pref

    with open(prefFile) as f:
        for line in f:
            pref.append((line.split('=')[1]).strip())
    
    # If the machineID in preferences file is different from the newly generated one, write the new machine ID to preferences file
    if pref[2] != machineID:
        writeMachineID(machineID)

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
    machineID = machineHash.hexdigest()[0:32]

    # Now let's crosscheck the preferences file
    readPreferences()


# Generates machine ID for Windows based systems
def generateForWindows():
    # first storage drive's serial number
    storageCMD = "wmic DISKDRIVE get SerialNumber"
    sysStorage = subprocess.check_output(storageCMD).decode().split('\n')[1].strip()

    # system's UUID
    uuidCMD = "wmic csproduct get UUID"
    sysUUID = subprocess.check_output(uuidCMD).decode().split('\n')[1].strip()

    # system's hardware address as a 48-bit positive integer
    sysMACAddr = uuid.getnode()

    # create a new sha3_512 object
    machineHash = hashlib.sha3_512()
    # encode as utf-8 and add storage serial number, system UUID and MAC address and hash it
    machineHash.update(str(sysStorage).encode('utf-8') + str(sysUUID).encode('utf-8') + str(sysMACAddr).encode('utf-8'))

    # truncate and store the hexdigest as machineID
    global machineID
    machineID = machineHash.hexdigest()[0:32]

    # Now let's crosscheck the preferences file
    readPreferences()


# Generates machine ID for Linux based systems
def generateForLinux():
    # first storage drive's serial number
    storageCMD = "lsblk --nodeps -no serial"
    sysStorage,error = subprocess.Popen(storageCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sysStorage = sysStorage.decode().split('\n')[0].strip()

    # system's UUID from message buffer of the kernel
    uuidCMD = 'dmesg | grep UUID | grep "Kernel" | sed "s/.*UUID=//g" | sed "s/\ ro\ quiet.*//g"'
    sysUUID,error = subprocess.Popen(uuidCMD, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sysUUID = sysUUID.decode().split(' ')[0].strip()

    # system's hardware address as a 48-bit positive integer
    sysMACAddr = uuid.getnode()

    # create a new sha3_512 object
    machineHash = hashlib.sha3_512()
    # encode as utf-8 and add storage serial number, system UUID and MAC address and hash it
    machineHash.update(str(sysStorage).encode('utf-8') + str(sysUUID).encode('utf-8') + str(sysMACAddr).encode('utf-8'))

    # truncate and store the hexdigest as machineID
    global machineID
    machineID = machineHash.hexdigest()[0:32]

    # Now let's crosscheck the preferences file
    readPreferences()


# Writes the new machine ID to the preferences file
def writeMachineID(newID):

    userPreferences = open(prefFile, 'w')
    userPreferences.write('numberOfLogs=' + str(pref[0]) + '\ncollectionFrequency=' + str(pref[1]) + '\nmachineID=' + str(newID))
    userPreferences.close()

if __name__ == '__main__':
    generateMachineID()
