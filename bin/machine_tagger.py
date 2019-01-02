import hashlib
import os
import platform
import subprocess
import uuid

# Global variables to hold reused values across the program
machine_Id = ''
preferences = []
user_preferences = 'preferences.conf'


# Reading the preferences file and writing machineID if it looks different
def read_preferences():
   
    global machine_Id
    global preferences

    with open(user_preferences) as f:
        for line in f:
            preferences.append((line.split('=')[1]).strip())
    
    # If the machineID in preferences file is different from the newly generated one, write the new machine ID to preferences file
    if preferences[2] != machine_Id:
        write_machine_Id(machine_Id)

# Identifying the operating system and calling appropriate function to generate the machine ID
def generate_machine_Id():
    
    my_sys = platform.system()

    if my_sys == 'Windows':
        generate_for_windows()
    elif my_sys == 'Darwin':
        generate_for_mac_os()
    elif my_sys == 'Linux':
        generate_for_linux()


# Generates machine ID for macOS based systems
def generate_for_mac_os():
    # first storage drive's serial number
    storage_cmd = "/usr/sbin/diskutil info / | /usr/bin/awk '$0 ~ /UUID/ { print $3 }'"
    sys_storage,error = subprocess.Popen(storage_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sys_storage = sys_storage.decode().split('\n')[0].strip()

    # system's serial number
    uuid_cmd = "system_profiler SPHardwareDataType | grep -i 'Serial Number (system):' | awk '{print $4}'"
    sys_uuid,error = subprocess.Popen(uuid_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sys_uuid = sys_uuid.decode().split('\n')[0].strip()

    # system's hardware address as a 48-bit positive integer
    sys_mac_addr = uuid.getnode()

    # create a new sha3_512 object
    machine_hash = hashlib.sha3_512()
    # encode as utf-8 and add storage serial number, system UUID and MAC address and hash it
    machine_hash.update(str(sys_storage).encode('utf-8') + str(sys_uuid).encode('utf-8') + str(sys_mac_addr).encode('utf-8'))

    # truncate and store the hexdigest as machineID
    global machine_Id
    machine_Id = machine_hash.hexdigest()[0:32]

    # Now let's crosscheck the preferences file
    read_preferences()


# Generates machine ID for Windows based systems
def generate_for_windows():
    # first storage drive's serial number
    storage_cmd = "wmic DISKDRIVE get SerialNumber"
    sys_storage = subprocess.check_output(storage_cmd).decode().split('\n')[1].strip()

    # system's UUID
    uuid_cmd = "wmic csproduct get UUID"
    sys_uuid = subprocess.check_output(uuid_cmd).decode().split('\n')[1].strip()

    # system's hardware address as a 48-bit positive integer
    sys_mac_addr = uuid.getnode()

    # create a new sha3_512 object
    machine_hash = hashlib.sha3_512()
    # encode as utf-8 and add storage serial number, system UUID and MAC address and hash it
    machine_hash.update(str(sys_storage).encode('utf-8') + str(sys_uuid).encode('utf-8') + str(sys_mac_addr).encode('utf-8'))

    # truncate and store the hexdigest as machineID
    global machine_Id
    machine_Id = machine_hash.hexdigest()[0:32]

    # Now let's crosscheck the preferences file
    read_preferences()


# Generates machine ID for Linux based systems
def generate_for_linux():
    # first storage drive's serial number
    storage_cmd = "lsblk --nodeps -no serial"
    sys_storage,error = subprocess.Popen(storage_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sys_storage = sys_storage.decode().split('\n')[0].strip()

    # system's UUID from message buffer of the kernel
    uuid_cmd = 'dmesg | grep UUID | grep "Kernel" | sed "s/.*UUID=//g" | sed "s/\ ro\ quiet.*//g"'
    sys_uuid,error = subprocess.Popen(uuid_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).communicate()
    sys_uuid = sys_uuid.decode().split(' ')[0].strip()

    # system's hardware address as a 48-bit positive integer
    sys_mac_addr = uuid.getnode()

    # create a new sha3_512 object
    machine_hash = hashlib.sha3_512()
    # encode as utf-8 and add storage serial number, system UUID and MAC address and hash it
    machine_hash.update(str(sys_storage).encode('utf-8') + str(sys_uuid).encode('utf-8') + str(sys_mac_addr).encode('utf-8'))

    # truncate and store the hexdigest as machineID
    global machine_Id
    machine_Id = machine_hash.hexdigest()[0:32]

    # Now let's crosscheck the preferences file
    read_preferences()


# Writes the new machine ID to the preferences file
def write_machine_Id(new_id):

    user_pref = open(user_preferences, 'w')
    user_pref.write('logs_to_collect=' + str(preferences[0]) + '\nlog_frequency=' + str(preferences[1]) + '\nmachine_Id=' + str(new_id))
    user_pref.close()

if __name__ == '__main__':
    generate_machine_Id()