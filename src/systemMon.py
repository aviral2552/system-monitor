###
# Simple cross-platform python script to monitor and capture CPU, memory, sensor and battery information etc
#
# Author: https://github.com/thelamehacker
# Last update: 23 October 2018
# Version: 0.2a
#
# References:
# https://psutil.readthedocs.io/en/latest/#other-system-info
# http://code.activestate.com/recipes/578019
#
###

import os
import sys
import psutil
import time
import datetime
import socket
import threading

separator = "-" * 80

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

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

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

def secs2hours(secs):
    mm, ss = divmod(secs, 60)
    hh, mm = divmod(mm, 60)
    return "%d:%02d:%02d" % (hh, mm, ss)

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
    
    f.write("\nDumped {} processes successfully and couldn't access {} processes due to insufficient privileges.".format(access, noAccess))
    f.close()

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

def captureBatteryState():
    
    logPath = str('battery.log')
    f = open(logPath, 'a')

    f.write("\n\n" + separator + "\n")
    f.write(time.ctime() + "\n")

    if not hasattr(psutil, "sensors_battery"):
        f.write("\nPlatform or system is not supported.\n")
    batt = psutil.sensors_battery()
    if batt is None:
        f.write("\nBattery not deteced.\n")

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

def captureDiskState():

    logPath = str('disks.log')
    f = open(logPath, 'a')

    f.write("\n\n" + separator + "\n")
    f.write(time.ctime() + "\n")

    templ = "%-17s %8s %8s %8s %5s%% %9s  %s"
    f.write(templ % ("Device", "Total", "Used", "Free", "Use ", "Type",
                   "Mount"))
    for part in psutil.disk_partitions(all=False):
        if os.name == 'nt':
            if 'cdrom' in part.opts or part.fstype == '':
                # skip cd-rom drives with no disk in it; they may raise
                # ENOENT, pop-up a Windows GUI error for a non-ready
                # partition or just hang.
                continue
        usage = psutil.disk_usage(part.mountpoint)
        f.write("\n")
        f.write(templ % (
            part.device,
            bytes2human(usage.total),
            bytes2human(usage.used),
            bytes2human(usage.free),
            int(usage.percent),
            part.fstype,
            part.mountpoint))
    f.close()

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

def bootTime():
    logPath = str('bootTime.log')
    f = open(logPath, 'a')

    f.write("\n\n" + separator + "\n")
    f.write(time.ctime() + "\n")
    f.write("\nCurrent system boot time is: " + datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S"))
    f.close()

def mainProg():
    ## Main program
    if not os.path.isdir("logs"):
        os.system('mkdir logs')
    
    os.chdir('logs')
    
    currentDate = str(datetime.date.today())
    if not os.path.isdir(currentDate):
        os.system('mkdir ' + currentDate)
    
    os.chdir(currentDate)

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
    
    ## Run the entire script every 5 minutes for next 5 hours
    
    maxTime = int(input("How many times would you like me to collect the logs: "))
    freq = int(input("At what frequency should I collect the logs? Every (in seconds): "))
    i = 1

    currentDirectory = os.getcwd()
    spinner = Spinner()

    while i <= maxTime:
        mainProg()
        os.chdir(currentDirectory)
        print("Run #%i completed! Time remaining till next run: " % i)
        spinner.start()
        countdown(freq)
        time.sleep(freq)
        spinner.stop()
        i += 1