###
# Simple cross-platform python script to monitor and capture CPU, memory, network, sensor and battery information 
# Part of Project Aradia
#
# Last update: 29 January 2019
# Version: 0.5c
#
###

import datetime
import json
import os
import platform
import socket
import sys
import threading
import time
import numpy as np

import psutil
import requests

import db_writer

logs_to_collect = 0
log_frequency = 0
machine_Id = ''
user_preferences = 'preferences.conf'

# For console output formatting, asthetics and reading/writing user preferences
class set_run_env:

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
    @staticmethod
    def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    # To display the countdown till next run of log captures on the console.
    @staticmethod
    def countdown(t):
        while t:
            mins, secs = divmod(t, 60)
            time_format = '{:02d}:{:02d}'.format(mins, secs)
            print(time_format, end='\r')
            time.sleep(1)
            t -= 1

    @staticmethod
    def yes_no(check_me):
        if check_me == 'y' or check_me == 'Y' or check_me == 'yes' or check_me == 'Yes' or check_me == 'YES':
            return True

    @staticmethod
    def read_preferences():

        global logs_to_collect, log_frequency, user_preferences, machine_Id
        preferences = []

        with open(user_preferences) as f:
            for line in f:
                preferences.append((line.split('=')[1]).strip())
            preferences[0] = int(preferences[0])
            preferences[1] = int(preferences[1])
        machine_Id = str(preferences[2])

        print('Current runtime config\n======================\n\nLogs to collect: %i\nCollection frequency (in seconds): %i' %(preferences[0], preferences[1]))
        
        print('\nWould you like to start logging with the default configuration? (Y/n): ')

        if set_run_env.yes_no(input().strip()):
            logs_to_collect = preferences[0]
            log_frequency = preferences[1]
        else:
            logs_to_collect = int(input('\nHow many times would you like me to collect the logs: '))
            log_frequency = int(input('At what frequency should I collect the logs? Every (in seconds): '))
            print('\nNew runtime preferences will be saved and the logging will start now.')
            f = open(user_preferences, 'w')
            f.write('logs_to_collect=' + str(logs_to_collect) + '\nlog_frequency=' + str(log_frequency) + '\nmachine_Id=' + str(preferences[2]))
            f.close()
            time.sleep(3)

class flow_controller:

    def __init__(self, logs_to_collect, log_frequency, user_preferences):
        self.logs_to_collect = logs_to_collect
        self.log_frequency = log_frequency
        self.user_preferences = user_preferences

    def initiator(self):
        run_env = set_run_env()
        
        i = 1
        # Run the program at specified frequency and number of times. And a touch of some nice console output magic.
        while i <= logs_to_collect:
            data_store = log_collector()
            data_store.collect_all_data()
            run_env.clear_screen()
            print('Statistics\n==========\n\nTotal logs to collect: %i\nWait interval (in seconds): %i' % (self.logs_to_collect, self.log_frequency))
            print('\nLogs collected: %i\nLogs remaining: %i\n' % (i, self.logs_to_collect - i))
            if i != self.logs_to_collect:
                print('Countdown to next log collection: ')
                run_env.start()
                run_env.countdown(self.log_frequency)
                run_env.stop()
            else:
                run_env.clear_screen()
                print('All logs have been captured.\n')
                data_store.send_to_db_writer()

            i += 1        
        
class log_collector:

    def __init__(self):
        self.system_data = []
        self.disk_data = []
        self.battery_data = []
        self.process_data = []
        self.network_data = []

        self.disk_data_array = []
        self.network_data_array = []
        self.process_data_array = []

    def system_info(self):

        try:
            os_map = {
            'POSIX': psutil.POSIX, 'Windows': psutil.WINDOWS, 'Linux': psutil.LINUX,
            'macOS': psutil.MACOS, 'FreeBSD': psutil.FREEBSD, 'NetBSD': psutil.NETBSD,
            'OpenBSD': psutil.OPENBSD, 'BSD': psutil.BSD, 'Sun OS': psutil.SUNOS,
            'AIX': psutil.AIX
            }
            set_os = 'unknown'
        except:
            os_map = {
            'POSIX': psutil.POSIX, 'Windows': psutil.WINDOWS, 'Linux': psutil.LINUX,
            'macOS': psutil.OSX, 'FreeBSD': psutil.FREEBSD, 'NetBSD': psutil.NETBSD,
            'OpenBSD': psutil.OPENBSD, 'BSD': psutil.BSD, 'Sun OS': psutil.SUNOS,
            'AIX': psutil.AIX
            }
            set_os = 'unknown'

        for key, value in os_map.items():
            if value == True:
                set_os = str(key)
        
        self.system_data.append(machine_Id + '[' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ']')
        self.system_data.append(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.system_data.append(datetime.datetime.now().strftime('%H:%M:%S'))
        self.system_data.append(set_os)
        self.system_data.append(str(platform.release()))
        self.system_data.append(str(platform.platform()))
        self.system_data.append(str(platform.version()))
        self.system_data.append(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d'))
        self.system_data.append(datetime.datetime.fromtimestamp(psutil.boot_time()).strftime('%H:%M:%S'))

        try:
            geo_ip_data = requests.get('https://get.geojs.io/v1/ip/geo.json').json()
        
            for value in geo_ip_data.values():
                self.system_data.append(value)
            
        except:
            for _ in range(15):
                self.system_data.append('')

        # Tip: Access geo_ip_data to see the entire dict for constructing column names in the database

    def disk_state(self):

        for part in psutil.disk_partitions(all=False):
            if os.name == 'nt':
                if 'cdrom' in part.opts or part.fstype == '':
                    # skip cd-rom drives with no disk in it
                    continue
            usage = psutil.disk_usage(part.mountpoint)
        
            self.disk_data.append(datetime.datetime.now().strftime('%Y-%m-%d'))
            self.disk_data.append(datetime.datetime.now().strftime('%H:%M:%S'))
            self.disk_data.append(str(part.device))
            self.disk_data.append(str(usage.total))
            self.disk_data.append(str(usage.used))
            self.disk_data.append(str(usage.free))
            self.disk_data.append(str(int(usage.percent)))
            self.disk_data.append(str(part.fstype))
            self.disk_data.append(str(part.mountpoint))

        self.disk_data_array = np.asarray(self.disk_data)
        self.disk_data_array = self.disk_data_array.reshape(int(len(self.disk_data) / 9), 9)

    def battery_state(self):

        self.battery_data.append(datetime.datetime.now().strftime('%Y-%m-%d'))
        self.battery_data.append(datetime.datetime.now().strftime('%H:%M:%S'))

        if not hasattr(psutil, 'sensors_battery'):
            self.battery_data.append('no')
        else:
            self.battery_data.append('yes')

        batt = psutil.sensors_battery()

        if batt is None:
            self.battery_data.append('no')
        else:
            self.battery_data.append('yes')

        self.battery_data.append(str(round(batt.percent, 2)))

        if batt.power_plugged:
            # Unlimited juice.... as per psutil apparently
            self.battery_data.append('unlimited')
            if batt.percent < 100:
                self.battery_data.append('charging')
            else:
                self.battery_data.append('charged')
            self.battery_data.append('yes')
        else:
            self.battery_data.append(str(batt.secsleft))
            self.battery_data.append('discharging')
            self.battery_data.append('no')

    def process_state(self):

        for proc in psutil.process_iter():
            try:
                self.process_data.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                self.process_data.append(datetime.datetime.now().strftime('%H:%M:%S'))

                try:
                    self.process_data.append(str(proc.pid))
                except:
                    self.process_data.append('')

                try:
                    self.process_data.append(str(proc.ppid()))
                except:
                    self.process_data.append('')
                
                try:
                    self.process_data.append(str(proc.name()))
                except:
                    self.process_data.append('')
                
                try:
                    self.process_data.append(str(proc.cpu_percent()/psutil.cpu_count()))
                except:
                    self.process_data.append('')

                try:
                    self.process_data.append(str(proc.memory_percent(memtype='rss')))
                except:
                    self.process_data.append('')

                try:
                    self.process_data.append(str(proc.memory_info().rss))
                except:
                    self.process_data.append('')

                try:    
                    self.process_data.append(str(proc.memory_info().vms))
                except:
                    self.process_data.append('')

                try:
                    self.process_data.append(str(proc.exe()))
                except:
                    self.process_data.append('')

                try:    
                    self.process_data.append(str(proc.username()))
                except:
                    self.process_data.append('')
                
                try:
                    self.process_data.append(str(proc.nice()))
                except:
                    self.process_data.append('')

            except psutil.AccessDenied:
                pass

        self.process_data_array = np.asarray(self.process_data)
        self.process_data_array = self.process_data_array.reshape(int(len(self.process_data)/12), 12)

    def network_state(self):

        stats = psutil.net_if_stats()
        io_counters = psutil.net_io_counters(pernic=True)

        # For iterating through IPv4/IPv6/MAC addresses
        afMap = {
        socket.AF_INET: 'IPv4',
        socket.AF_INET6: 'IPv6',
        psutil.AF_LINK: 'MAC',
        }

        # For looking up duplex state
        duplexMap = {
            psutil.NIC_DUPLEX_FULL: 'full',
            psutil.NIC_DUPLEX_HALF: 'half',
            psutil.NIC_DUPLEX_UNKNOWN: 'unknown',
        }

        for nic, addrs in psutil.net_if_addrs().items():
            keep_count = 0

            for addr in addrs:
                if addr.address is not None:
                    keep_count += 1

            if keep_count == 3:
                self.network_data.append(datetime.datetime.now().strftime('%Y-%m-%d'))
                self.network_data.append(datetime.datetime.now().strftime('%H:%M:%S'))
                self.network_data.append(str(nic))
                if nic in stats:
                    st = stats[nic]
                if st.isup is not None:
                    self.network_data.append('yes')
                else:
                    self.network_data.append('no')
                self.network_data.append(str(st.speed))
                self.network_data.append(str(duplexMap[st.duplex]))
                self.network_data.append(str(st.mtu))

                if nic in io_counters:
                    io = io_counters[nic]

                    self.network_data.append(str(io.bytes_recv))
                    self.network_data.append(str(io.packets_recv))
                    self.network_data.append(str(io.errin))
                    self.network_data.append(str(io.dropin))

                    self.network_data.append(str(io.bytes_recv))
                    self.network_data.append(str(io.packets_sent))
                    self.network_data.append(str(io.errout))
                    self.network_data.append(str(io.dropout))
                
                address_bugfix = 0
                for addr in addrs:
                    current_addr = str(afMap.get(addr.family, addr.family))

                    # For IPv4 addresses
                    if current_addr.startswith('IPv4', 0, 3) and address_bugfix == 0:
                        self.network_data.append(str(addr.address))
                        address_bugfix += 1
                
                    # For MAC addresses
                    elif current_addr.startswith('MAC', 0, 2) and address_bugfix == 1:
                        self.network_data.append(str(addr.address))
                        address_bugfix += 1
                    
                    # For IPv6 addresses
                    elif current_addr.startswith('IPv6', 0, 3) and address_bugfix == 2:
                        self.network_data.append(str(addr.address))
                        address_bugfix += 1

                    # Filling blank values for missing addresses (IPv4/MAC/IPv6)
                    if address_bugfix != 3:
                        while address_bugfix < 3:
                            self.network_data.append('')
                            address_bugfix += 1
                    
                    if addr.broadcast:
                        self.network_data.append(str(addr.broadcast))
                    else:
                        self.network_data.append('')

                    if addr.netmask:
                        self.network_data.append(str(addr.netmask))
                    else:
                        self.network_data.append('')

                    if addr.ptp:
                        self.network_data.append(str(addr.ptp))
                    else:
                        self.network_data.append('')
                
        self.network_data_array = np.asarray(self.network_data)
        num_of_adapters = int(len(self.network_data) / 27)
        self.network_data_array = self.network_data_array.reshape(num_of_adapters, 27)

    def collect_all_data(self):
        self.system_info()
        self.disk_state()
        self.battery_state()
        self.process_state()
        self.network_state()

    def send_to_db_writer(self):
        db_writer.start_program(self.system_data, self.disk_data_array, self.battery_data, self.network_data_array, self.process_data)
        #print(self.system_data)
        #print(self.disk_data_array)
        #print(self.battery_data)
        #print(self.network_data_array)
        #print(self.process_data_array)

def start_program():
    set_run_env.read_preferences()
    start_collecting = flow_controller(logs_to_collect, log_frequency, user_preferences)
    start_collecting.initiator()

if __name__ == '__main__':
    start_program()