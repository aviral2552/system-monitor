
#############################################################
# networkIntClean.py for systemMon.py
# purpose: to parse with machineID gen from machineTagger
# authors: ld, lh
# updated: 2018-11-19
#############################################################
import pandas as pd
import csv
import re
import datetime


#function to define structure of logID
def format_logId_net():
    if log_count <= 9 and log_count >= 0:
        placeholder = '000'
    elif log_count <= 99 and log_count >= 10:
        placeholder = '00'
    elif log_count > 99:
        placeholder = '0'
    date = (timeStamp[13:23])
    uniqueLogId.append(machineID + str(date) + '[' + placeholder + str(log_count + 1) + ']')

def day():
    s = df[1]
    s2 = s[1:]
    df[1] = pd.to_datetime(s2)
    df['day'] = df[1].dt.dayofweek
    df.iloc[0, 1] = "timeStamp"
    df.iloc[0, 23] = "dayofweek"

machineID = '327d87e2c8870aed161afea1ef803dc4'
captureTime = ['timeStamp']
name = ['name']
active= ['active']
speed= ['speed']
duplex = ['duplex']
mtu = ['mtu']
incomingBytes = ['incomingBytes']
incomingPackets = ['incomingPackets']
incomingErrors = ['incomingErrors']
incomingDrops = ['incomingDrops']
outgoingBytes = ['outgoingBytes']
outgoingPackets = ['outgoingPackets']
outgoingErrors = ['outgoingErrors']
outgoingDrops = ['outgoingDrops']
IPv4= ['IPv4']
IPv4_netmask = ['IPv4_netmask']
IPv4_broadcast=['IPv4_broadcast']
IPv4_p2p=['IPv4_p2p']
IPv6 = ['IPv6']
IPv6_netmask = ['IPv6_netmask']
IPv6_broadcast=['IPv6_broadcast']
IPv6_p2p=['IPv6_p2p']
uniqueLogId=['LogID']

netmaskIPv4 = 0
netmaskIPv6 = 0
broadcastIPv4 = 0
broadcastIPv6 = 0
p2pIPv4 = 0
p2pIPv6 = 0

#this logic and area may be a good place to manage missing data with certain fields (columns)
log_count = 0   # For holding number of logs
timestampFix = 0
timeStamp =''

with open('networkInterfaces.log') as f:
    for line in f:
        if line.startswith('</log>') == True:
            log_count += 1

        if line.startswith('<MAC>') == True:
            continue

        if line.startswith('<captureTime>') == True:
            timeStamp = line

        if line.startswith('<name>') == True:
            name.append(line)
            captureTime.append(timeStamp)
            timestampFix += 1
            format_logId_net()


        elif line.startswith('<active>') == True:
            active.append(line)

        elif line.startswith('<speed>') == True:
            speed.append(line)

        elif line.startswith('<duplex>') == True:
            duplex.append(line)

        elif line.startswith('<mtu>') == True:
            mtu.append(line)

        elif line.startswith('<incomingBytes>') == True:
            incomingBytes.append(line)

        elif line.startswith('<incomingPackets>') == True:
            incomingPackets.append(line)

        elif line.startswith('<incomingErrors>') == True:
            incomingErrors.append(line)

        elif line.startswith('<incomingDrops>') == True:
            incomingDrops.append(line)

        elif line.startswith('<outgoingBytes>') == True:
            outgoingBytes.append(line)

        elif line.startswith('<outgoingPackets>') == True:
            outgoingPackets.append(line)

        elif line.startswith('<outgoingErrors>') == True:
            outgoingErrors.append(line)

        elif line.startswith('<outgoingErrors>') == True:
            outgoingErrors.append(line)

        elif line.startswith('<outgoingDrops>') == True:
            outgoingDrops.append(line)

        elif line.startswith('<IPv4>') == True:
            IPv4.append(line)

        elif line.startswith('<IPv4_netmask>') == True:
            IPv4_netmask.append(line)

        elif line.startswith('<IPv4_netmask>') == True:
            netmaskIPv4 = 1
            IPv4_netmask.append(line)

        elif line.startswith('<IPv6>') == True:
            IPv6.append(line)

        elif line.startswith('<IPv6_netmask>') == True:
            IPv6_netmask.append(line)

        elif line.startswith('<IPv4_broadcast>') == True:
            broadcastIPv4 = 1
            IPv4_broadcast.append(line)

        elif line.startswith('<IPv4_p2p>') == True:
            IPv4_p2p.append(line)

        if line.startswith('</log>') == True:
            if netmaskIPv4 == 0:
                IPv4_netmask.append('')
            if broadcastIPv4 == 0:
                IPv4_broadcast.append('')
            if netmaskIPv6 == 0:
                IPv6_netmask.append('')
            if broadcastIPv6 == 0:
                IPv6_broadcast.append('')
            if p2pIPv4 == 0:
                IPv4_p2p.append('')
            if p2pIPv6 == 0:
                IPv6_p2p.append('')



df = pd.DataFrame(
    list(zip(uniqueLogId, captureTime, name, active, speed, duplex, mtu, incomingBytes, incomingPackets, incomingErrors,
             incomingDrops, outgoingBytes, outgoingPackets, outgoingErrors, outgoingDrops, IPv4, IPv4_netmask, IPv4_broadcast,
             IPv4_p2p, IPv6, IPv6_netmask, IPv6_broadcast, IPv6_p2p)))


stuffToIgnore = ['<captureTime>', '</captureTime>', '<name>', '</name>', '<speed>', '</speed>',
                 '<active>', '</active>', '<duplex>', '</duplex>', '<mtu>', '</mtu>',
                 '<incomingBytes>', '</incomingBytes>', '<incomingPackets>', '</incomingPackets>', '<incomingErrors>',
                 '</incomingErrors>',
                 '<incomingDrops>', '</incomingDrops>', '<outgoingBytes>', '</outgoingBytes>', '<outgoingPackets>',
                 '</outgoingPackets>', '<outgoingErrors>', '</outgoingErrors>', '<outgoingDrops>', '</outgoingDrops>',
                 '<IPv4>', '</IPv4>', '<IPv4_netmask>', '</IPv4_netmask>', '<IPv6>', '</IPv6>', '<IPv6_netmask>',
                 '</IPv6_netmask>', '<MAC>', '</MAC>', '<IPv4_broadcast>', '</IPv4_broadcast>', '<IPv4_p2p>',
                 '</IPv4_p2p>'
                 ]

# needed to add a separate line for \n removal cause it wasn't working in the stuffToIgnore
df = df.replace("\n", "", regex=True)
for stuff in stuffToIgnore:
    df = df.replace(stuff, "", regex=True)

day()

df.to_csv('networkInterfaces.csv', index=False, header=False)

print(df)