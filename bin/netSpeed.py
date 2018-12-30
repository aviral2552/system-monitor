###
# Simple cross-platform python script to monitor and print current
# network speed for specified network interface on the console
#
# Part of Project Aradia
#
# Author: Lame Hacker (https://github.com/thelamehacker)
# Last update: 1 November 2018
# Version: 0.1
#
###

import collections
import os
import threading
import time
import psutil

# Setting target interface
# In future, we will iterate through interfaces from psutil.net_io_counters
# And create a thread for each interface where computer has an assigned IPv4 address (active connection)
# Every thread will then write to a log file with <undefined_frequency> along with a total UL/DL speed for <undefined_time>
targetInterface = 'en8'

# Set frequency for speed collection in seconds
collectionFreq = 1

# Housekeeping on the console
# Detects the OS and runs appropriate clear screen command.
def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def calc_ul_dl(rate, collectionFreq, interface):
        # Capturing current timestamp
        t0 = time.time()

        # Getting current data consumption for the 'interface' and store in tot
        counter = psutil.net_io_counters(pernic=True)[interface]
        tot = (counter.bytes_sent, counter.bytes_recv)

        # Keep refreshing the data consumption every 'collectionFreq' seconds
        while True:
                # Copying the current consumption last_tot
                last_tot = tot

                # Waiting for the 'collectionFreq' seconds
                time.sleep(collectionFreq)

                # Refreshing current consumption after 'collectionFreq' seconds
                counter = psutil.net_io_counters(pernic=True)[interface]
                # Updating timestamp
                t1 = time.time()

                # Getting current data consumption for the 'interface' and store in tot
                tot = (counter.bytes_sent, counter.bytes_recv)

                # Subtracting current consumtption (tot) from last consumption (last_tot) and storing in the deque (rate)
                ul, dl = [(now - last) / (t1 - t0) / 1000.0
                        for now, last in zip(tot, last_tot)]
                rate.append((ul, dl))

                # Updating timestamp
                t0 = time.time()

# Simple printing of current UL/DL values in 'rate'
def print_rate(rate):
    try:
        print('Active interface: %s' %targetInterface)
        print(time.ctime() + ' || ' + 'UL: {0:.0f} kB/s / DL: {1:.0f} kB/s'.format(*rate[-1]))
    except IndexError:
        'UL: - kB/s/ DL: - kB/s'

def createThread(rate):
        
        # Create the ul/dl thread and passing arguments to execute 'calc_ul_dl' function
        t = threading.Thread(target=calc_ul_dl, args=(rate, collectionFreq, targetInterface))

        # The program will exit if there are only daemonic threads left
        t.daemon = True
        t.start()


if __name__ == '__main__':
        
        # Create a deque of length 1 to hold the UL/DL values
        transfer_rate = collections.deque(maxlen=1)

        # Calling the function to create thread(s)
        createThread(transfer_rate)

        # Print current values every 'printFreq' second on the console
        printFreq = 1
        while True:
                #print("Interface: %s" %targetInterface)
                print_rate(transfer_rate)
                time.sleep(printFreq)
                clearScreen()