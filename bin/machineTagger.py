import platform

machineID = 0
pref = []
prefFile = str('preferences.cfg')

# Reading the preferences file and generating machine ID if the value is 0

def readPreferences():
   
    global machineID
    global pref

    with open(prefFile) as f:
        for line in f:
            pref.append(int((line.split('=')[1]).strip()))
    
    if pref[2] == 0:
        generateMachineID()

# Identifying the operating system and calling appropriate function to generate the machine ID
def generateMachineID():
    
    mySys = platform.system()

    if mySys == 'Darwin':
        generateForMacOS()
    elif mySys == 'Windows':
        generateForWindows()
    elif mySys == 'Linux':
        generateForLinux()

# Generates machine ID for macOS based systems

def generateForMacOS():
    print('Placeholder')

# Generates machine ID for Windows based systems

def generateForWindows():
    print('Placeholder')

# Generates machine ID for Linux based systems

def generateForLinux():
    print('Placeholder')

# Writes the new machine ID to the preferences file

def writeMachineID(newID):

    f = open(prefFile, 'w')
    f.write('numOfLogs=' + str(pref[0]) + '\nfreq=' + str(pref[1]) + '\nmachineID=' + str(newID))
    f.close()

if __name__ == '__main__':
    readPreferences()