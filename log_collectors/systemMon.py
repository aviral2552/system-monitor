###
# Simple cross-platform python script to monitor and capture CPU, memory, sensor and battery information etc
# Part of Project Aradia
#
# Author: Lame Hacker (https://github.com/thelamehacker)
# Last update: 30 October 2018
# Version: 0.2a
#
# Attributions:
# https://psutil.readthedocs.io/en/latest/#other-system-info
# http://code.activestate.com/recipes/578019
#
###

# For navigating directories.
import os
import sys

# For capturing most data points.
# Intentionally not using anything else other than psutil to maintain cross-platform compatibility.
import psutil

# Logs must come with time. Hence, time must be imported. No bargaining here.
import time
import datetime

# For capturing network interfaces data.
import socket

# For multi-threading support.
# Currently only being used to run a spinner at console while waiting.
# Future implementation may include a consistent network bandwidth monitor, running in a separate thread.
import threading

# Standard separator of 80 neat hyphens for dividing captured logs in a day.
separator = "-" * 80

# For help with capturing network interfaces in captureNetworkInterfaces function.
af_map = {
    socket.AF_INET: 'IPv4',
    socket.AF_INET6: 'IPv6',
    psutil.AF_LINK: 'MAC',
}

duplex_map = {
    psutil.NIC_DUPLEX_FULL: "full",
    psutil.NIC_DUPLEX_HALF: "half",
    psutil.NIC_DUPLEX_UNKNOWN: "?",
}


# You spin my head right round, right round.
# On the console while waiting, right round round.
class Spinner:
    busy = False
    delay = 0.1

    @staticmethod
    def spinning_cursor():
        while 1: 
            for cursor in '|/-\\': yield cursor

    def __init__(self, delay=None):
        self.spinner_generator = self.spinning_cursor()
        if delay and float(delay): self.delay = delay

    def spinner_task(self):
        while self.busy:
            sys.stdout.write(next(self.spinner_generator))
            sys.stdout.flush()
            time.sleep(self.delay)
            sys.stdout.write('\b')
            sys.stdout.flush()

    def start(self):
        self.busy = True
        threading.Thread(target=self.spinner_task).start()

    def stop(self):
        self.busy = False
        time.sleep(self.delay)
        sys.stdout.write('\b')

# Housekeeping on the console
# Detects the OS and runs appropriate clear screen command.
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

# To display the countdown till next run of log captures on the console.
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

# Convert bytes to human readable format
# From - http://code.activestate.com/recipes/578019
def bytes2human(n):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

# Convert seconds to human readable format (HH:MM:SS).
# No AM/PM support to keep things consistent and reduce post processing during log cleaning and scraping.
def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

# To capture the current state of running processes on the system.
# Run the script as admin to capture more processes.
# Log will also write how many processes were inaccesible due to permission/access issues.
def captureProcessList():

    format = "%7s %7s %10s %7s %12s %12s %7s"
    format2 = "%8s %8s %7.2f %7.2f %12s %12s %7s"

    logPath = str('processes.log')
    f = open(logPath, 'a')
    f.write("\n\n" + separator + "\n")
    f.write(time.ctime() + "\n")
    f.write(format % ("PID", "NAME", "%CPU", "%MEM", "VMS", "RSS", "PATH"))
    f.write("\n")
    access = 0
    noAccess = 0

    for p in psutil.process_iter():
        try:
            pro_pid = p.pid
            name = p.name()
            cpu_percent = p.cpu_percent()/psutil.cpu_count()
            mem_percent = p.memory_percent(memtype="rss")
            rss  = str(p.memory_info().rss)
            vms = str(p.memory_info().vms)
            path = p.exe()

            f.write(format2 % (pro_pid, name, cpu_percent, mem_percent, vms, rss, path))
            access += 1
            f.write("\n")
        except psutil.AccessDenied:
            noAccess += 1
    
    f.write("\nDumped %i processes successfully and couldn't access %i processes due to insufficient privileges." %(access, noAccess))
    f.close()

# To check the temprature and fan sensors.
def captureSensorState():

    logPath = str('sensors.log')
    f = open(logPath, 'a')

    f.write("\n\n" + separator + "\n")
    f.write(time.ctime() + "\n")

    if hasattr(psutil, "sensors_temperatures"):
        temps = psutil.sensors_temperatures()
    else:
        temps = {}
    if hasattr(psutil, "sensors_fans"):
        fans = psutil.sensors_fans()
    else:
        fans = {}

    if not any((temps, fans)):
        f.write("\nCan't read any temperature or fan infomation.")

    names = set(list(temps.keys()) + list(fans.keys()))
    for name in names:
        f.write(name)
        # Temperatures.
        if name in temps:
            f.write("\n    Temperatures:")
            for entry in temps[name]:
                f.write("\n        %-20s %s°C (high=%s°C, critical=%s°C)" % (
                    entry.label or name, entry.current, entry.high,
                    entry.critical))
        # Fans.
        if name in fans:
            f.write("\n    Fans:")
            for entry in fans[name]:
                f.write("\n        %-20s %s RPM" % (
                    entry.label or name, entry.current))
        f.close()

# To capture current battery status including percentage, time left, charging state
def captureBatteryState():
    
    logPath = str('battery.log')
    f = open(logPath, 'a')

    f.write("\n\n" + separator + "\n")
    f.write(time.ctime() + "\n")

    if not hasattr(psutil, "sensors_battery"):
        f.write("\nPlatform or system is not supported.\n")
    batt = psutil.sensors_battery()
    if batt is None:
        f.write("\nBattery not detected.\n")

    f.write("\nCurrent charge:     %s%%" % round(batt.percent, 2))
    if batt.power_plugged:
        f.write("\nStatus:     %s" % (
            "Charging" if batt.percent < 100 else "Fully charged"))
        f.write("\nPlugged in: Yes")
    else:
        f.write("\nLeft:       %s" % secs2hours(batt.secsleft))
        f.write("\nStatus:     %s" % "Discharging")
        f.write("\nPlugged in: No")
    f.close()



    logPath = str('disks.log')
    f = open(logPath, 'a')

    f.write("\n<log>")
    f.write("\n<capturetime>" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "</capturetime>")

    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it
                continue
        usage = psutil.disk_usage(part.mountpoint)

        f.write("\n<name>" + str(part.device) + "</name>")
        f.write("\n<size>" + str(bytes2human(usage.total)) + "</size>")
        f.write("\n<used>" + str(bytes2human(usage.used)) + "</used>")
        f.write("\n<free>" + str(bytes2human(usage.free)) + "</free>")
        f.write("\n<%used>" + str(int(usage.percent)) + "</%used>")
        f.write("\n<fileSys>" + str(part.fstype) + "</fileSys>")
        f.write("\n<mountPoint>" + str(part.mountpoint) + "</mountPoint>")

    f.write("\n</log>\n")
    f.close()

# To capture state of all network interfaces
def captureNetworkInterfaces():

    logPath = str('networkInterfaces.log')
    f = open(logPath, 'a')

    f.write("\n\n" + separator + "\n")
    f.write(time.ctime() + "\n")

    stats = psutil.net_if_stats()
    io_counters = psutil.net_io_counters(pernic=True)
    for nic, addrs in psutil.net_if_addrs().items():
        f.write("\n%s:" % (nic))
        if nic in stats:
            st = stats[nic]
            f.write("\n    stats: ")
            f.write("\tspeed=%sMB, duplex=%s, mtu=%s, up=%s" % (
                st.speed, duplex_map[st.duplex], st.mtu,
                "yes" if st.isup else "no"))
        if nic in io_counters:
            io = io_counters[nic]
            f.write("\n    incoming: ")
            f.write("\tbytes=%s, pkts=%s, errs=%s, drops=%s" % (
                bytes2human(io.bytes_recv), io.packets_recv, io.errin,
                io.dropin))
            f.write("\n    outgoing: ")
            f.write("\tbytes=%s, pkts=%s, errs=%s, drops=%s" % (
                bytes2human(io.bytes_sent), io.packets_sent, io.errout,
                io.dropout))
        for addr in addrs:
            f.write("\n    %-4s" % af_map.get(addr.family, addr.family))
            f.write("address   : %s" % addr.address)
            if addr.broadcast:
                f.write("\n         broadcast : %s" % addr.broadcast)
            if addr.netmask:
                f.write("\n         netmask   : %s" % addr.netmask)
            if addr.ptp:
                f.write("\n      p2p       : %s" % addr.ptp)
        
    f.close()

# To capture disk and partition state
def captureDiskState():

# To check the system boot time
def bootTime():
    logPath = str('bootTime.log')
    f = open(logPath, 'a')

    f.write("\n<log>")
    f.write("\n<capturetime>" + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "</capturetime>")
    f.write("\n<boottime>" + datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S") + "</boottime>")
    f.write("\n</log>")
    f.close()

# The unofficial main function
def mainProg():

    # Check if 'logs' directory exist at current path
    # Create 'logs' directory if it doesn't already exist
    if not os.path.isdir('logs'):
        os.system('mkdir logs')
    
    # Navigate to 'logs' directory
    os.chdir('logs')
    
    # Check if there is already a directory with current date "YYYY-MM-DD" format
    # Create the directory if it doesn't exist
    currentDate = str(datetime.date.today())
    if not os.path.isdir(currentDate):
        os.system('mkdir ' + currentDate)
    
    # Navigate to the directory with current date
    # Reassigning and keeping the current date in 'currentDate' variable to overcome errors when date changes at midnight
    # and the program is still running. The program will continue capturing logs in the next date folder.
    os.chdir(currentDate)

    # A log file for track if the logs were successfully created.
    # TODO need to add error handling while calling the functions and write back to logTracker.log accordingly.
    logPath = str('logTracker.log')
    logTrack = open(logPath, 'a')
    logTrack.write("\n" + separator + "\n")

    logTrack.write("\nStart of capturing log at :" + time.ctime() + "\n\nCapturing...\n\n")

    bootTime()
    logTrack.write("System boot time\n")

    captureProcessList()
    logTrack.write("Running processes and resources used\n")

    captureDiskState()
    logTrack.write("Disk and partition information\n")

    captureNetworkInterfaces()
    logTrack.write("Network interfaces\n")

    captureSensorState()
    logTrack.write("Hardware sensors\n")

    captureBatteryState()
    logTrack.write("Battery state\n\nAll done!")


    logTrack.write("\n\nEnd of capturing log at: " + time.ctime() + "\n")
    logTrack.close()

if __name__ == '__main__':
    
    # Check with the user on the number of executions and frequency of log collection.
    numOfLogs = int(input("How many times would you like me to collect the logs: "))
    freq = int(input("At what frequency should I collect the logs? Every (in seconds): "))
    i = 1

    # Save the current directory to navigate back to avoid infinitely nested data folders.
    currentDirectory = os.getcwd()

    # New instance of "You spin my head right round, right round."
    spinner = Spinner()
    
    # Run the program at specified frequency and number of times. And a bit of nice console output.
    while i <= numOfLogs:
        mainProg()
        os.chdir(currentDirectory)
        clearScreen()
        print("Statistics\n==========\n\nTotal logs to collect: %i\nWait interval (in seconds): %i" % (numOfLogs, freq))
        print("\nLogs collected: %i\nLogs remaining: %i\n" % (i, numOfLogs - i))
        if i != numOfLogs:
            print("Countdown to next log collection: ")
            spinner.start()
            countdown(freq)
            spinner.stop()
        else:
            print("All logs have been captured and placed in \logs\%s\ directory.\n" % str(datetime.date.today()))
        i += 1