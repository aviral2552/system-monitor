###############################################################
# battery_check.py
# last updated 27.11.2018
# purpose : checks for discrepencies between cleaned and raw data.
# authors: calebpitts
################################################################

import pandas as pd
import os
import re
import glob
from collections import defaultdict

TAG_RE = re.compile(r'<[^>]+>')  # Regex constraint for removing XML tags


# Gets col data from excel files
def get_clean_cols(data_path, col_dict):
    df = pd.read_excel(io=data_path)

    # Puts column data into lists
    for col in list(df):
        col_list = df[col].tolist()
        col_dict[col] = col_list

    return col_dict


# Gets battery data from raw log file
def get_battery_data(dir, raw_dict):
    with open(dir) as file:
        for line in file:
            if line.startswith('<captureTime>'):
                raw_dict['captureTime'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<supported>'):
                raw_dict['supported'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<detected>'):
                raw_dict['detected'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<charge>'):
                raw_dict['charge'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<remaining>'):
                raw_dict['remaining'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<status>'):
                raw_dict['status'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags
            elif line.startswith('<plugged>'):
                raw_dict['plugged'].append((TAG_RE.sub('', line)).strip('\n'))  # strips XML tags

    return raw_dict


# Provides output and insight as to whether there are any discrepencies between the clean and raw data.
def compare_data(col_dict, raw_dict):
    try:
        print("Checking captureTime...")
        for num, (col, raw) in enumerate(zip(col_dict['Log time'], raw_dict['captureTime'])):
            # print("COL:", str(col), "- RAW:", str(raw))
            if raw != col:
                print("Discrepency in col 'captureTime' row", num)
                return

        print("Checking supported...")
        for num, (col, raw) in enumerate(zip(col_dict['Battery supported'], raw_dict['supported'])):
            # print("COL:", str(col), "- RAW:", str(raw))
            if raw != col:
                print("Discrepency in col 'supported' row", num)
                return

                print("Checking detected...")
        for num, (col, raw) in enumerate(zip(col_dict['Battery detected'], raw_dict['detected'])):
            # print("COL:", str(col), "- RAW:", str(raw))
            if raw != col:
                print("Discrepency in col 'detected' row", num)
                return

        print("Checking charge...")
        for num, (col, raw) in enumerate(zip(col_dict['Current charge'], raw_dict['charge'])):
            # print("COL:", str(col), "- RAW:", str(raw))
            if str(raw) != str(col):
                print("Discrepency in col 'charge' row", num)
                return

        print("Checking remaining...")
        for num, (col, raw) in enumerate(zip(col_dict['Battery reamining for'], raw_dict['remaining'])):
            # print("COL:", str(col), "- RAW:", str(raw))
            if raw != col:
                print("Discrepency in col 'remaining' row", num)
                return

        print("Checking status...")
        for num, (col, raw) in enumerate(zip(col_dict['Charging status'], raw_dict['status'])):
            # print("COL:", str(col), "- RAW:", str(raw))
            if raw != col:
                print("Discrepency in col 'status'' row", num)
                return

        print("Checking plugged...")
        for num, (col, raw) in enumerate(zip(col_dict['Plugged in'], raw_dict['plugged'])):
            # print("COL:", str(col), "- RAW:", str(raw))
            if raw != col:
                print("Discrepency in col 'plugged' row", num)
                return
        print("Battery logs and excel file match!!")  # Reaches end of try statement if no discrepencies found
    except TypeError:
        print("One of the columns had a different number of rows.")


def main():
    data_path = '../data/batteryLogs.xlsx'  # from the log dir
    log_path = '../logs'
    raw_dict = defaultdict(list)
    col_dict = defaultdict(list)

    col_dict = get_clean_cols(data_path, col_dict)  # TEMPORARY. Will iterate through all excel files later...
    os.chdir(log_path)

    # Listing all sub-directories for logs
    logSubDir = glob.glob('*', recursive=False)

    # Iterating through every sub-directory, finding all log files and running appropriate cleaner script
    for subDir in logSubDir:
        os.chdir(subDir)

        logFileList = []
        logFileList = glob.glob('*.log', recursive=False)

        # Iterates through logs for raw data collection.
        for logFile in logFileList:
            if logFile == 'battery.log':
                print('Running batteryLog check for date: ' + subDir)
                raw_dict = get_battery_data(str(os.getcwd()) + '/battery.log', raw_dict)

        os.chdir('../')

    compare_data(col_dict, raw_dict)


if __name__ == '__main__':
    main()