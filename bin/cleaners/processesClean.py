import pandas as pd
import csv
import re
import datetime

#function to define structure of logID different than boot and battery
def format_logId_pc():
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
    df.iloc[0, 12] = "dayofweek"

machineID = '327d87e2c8870aed161afea1ef803dc4'
captureTime = ['timeStamp']
pid = ['pid']
parentPID= ['parentPID']
name= ['name']
cpu = ['%cpu']
priority = ['priority']
mem = ['%mem']
vms = ['vms']
rss = ['rss']
user = ['user']
path= ['path']
uniqueLogId=['LogID'] 

log_count = 0   # For holding number of logs
timestampFix = 0
timeStamp =''

with open('processes.log') as f:
    for line in f:
        if line.startswith('</log>') == True:
            log_count += 1

            #for i in range(timestampFix):
                    #captureTime.append(timeStamp)
      
        if line.startswith('<captureTime>') == True:
            timeStamp = line
        
        if line.startswith('<pid>') == True:
            pid.append(line)
            captureTime.append(timeStamp)
            timestampFix += 1

            format_logId_pc()

        elif line.startswith('<parentPID>') == True:
            parentPID.append(line)
    
        elif line.startswith('<name>') == True:
            name.append(line)
                
        elif line.startswith('<%cpu>') == True:
            cpu.append(line)
   
        elif line.startswith('<priority>') == True:
            priority.append(line)
   
        elif line.startswith('<%mem>') == True:
            mem.append(line)
        
        elif line.startswith('<vms>') == True:
            vms.append(line)
        
        elif line.startswith('<rss>') == True:
            rss.append(line)
    
        elif line.startswith('<user>') == True:
            user.append(line)
    
        elif line.startswith('<path>') == True:
            path.append(line)       

df = pd.DataFrame(list(zip(uniqueLogId,captureTime, pid, parentPID, name, cpu, priority,mem,vms,rss,user,path)))
 

stuffToIgnore = ['<captureTime>', '</captureTime>','<pid>','</pid>','<parentPID>','</parentPID>','<name>','</name>',
                 '<%cpu>','</%cpu>','<priority>','</priority>', '<%mem>','</%mem>','<vms>','</vms>','<rss>','</rss>',
                 '<user>','</user>','<path>','</path>','\n']


for stuff in stuffToIgnore:
        df = df.replace(stuff, "", regex = True)

day()

df.to_csv('processes.csv', index = False, header = False)

print("\nTotal number of events recorded per log: %i " % log_count)

print(df)            