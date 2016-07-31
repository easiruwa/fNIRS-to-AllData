# Created by Eseosa Asiruwa, Summer of 2016
# Title: All Data File Conversion
# Purpose: This program takes data ouput from fNIRS devices and creates an 
#          all data file. This program works with either 2 files (one oxy and
#          deoxy) or 4 (2 oxy and 2 deoxy).
# How to Use: - Make sure the files you want to combine are in your current 
#               directory
#             - Run program 
#             - Resulting file will be in directory

import pandas as pd
import csv
import fnmatch
import os

def getfiles(patterns):
    data_files = []
    # Look through the current folder 
    for file in os.listdir('.'):
        # Try to match each file name with given pattern
        for pattern in patterns:
            if fnmatch.fnmatch(file, pattern):
                # If the file name matches, add to list
                data_files.append(file)
    return data_files

def combine():
    # Files to be found
    patterns = ['*Probe1_Oxy.csv','*Probe1_Deoxy.csv', '*Probe2_Oxy.csv',
    '*Probe2_Deoxy.csv']

    files = getfiles(patterns) # retrieve files from directory

    # Seperate files into their respective lists
    oxyfiles = []
    deoxyfiles = []

    for x in files:
        if 'Oxy' in x:
            oxyfiles.append(x)
        else:
            deoxyfiles.append(x)

    # Sort to make sure that Probe 1 files are always taken first
    oxyfiles.sort()
    deoxyfiles.sort() 

    # Getting the beginning number of the files
    num  = oxyfiles[0] 
    num = num.split('_',1)[0]
    outputfile = num + "_All_Data.csv"

    # Create a new file
    f = open(outputfile, "a")
    writer = csv.writer(f)

    # Get first set of oxy and deoxy data, format them
    first_set = oxyfiles.pop(0)
    first_set = format_file(first_set)

    second_set = deoxyfiles.pop(0)
    second_set = format_file(second_set)

    # Create a data frame, using pandas module, from the deoxy data
    # Label the first cell 
    first_deoxy_set = pd.DataFrame(second_set)
    first_deoxy_set[0][0] = 'Probe 1 deoxy'

    # Create a data frame for oxy
    # Label the first cell 
    first_oxy_set = pd.DataFrame(first_set)
    first_oxy_set[0][0] = 'Probe 1 oxy'

    # Combine oxy and deoxy data frames
    result = pd.concat([first_oxy_set,first_deoxy_set], axis=1)

    # Convert data frame to csv, remove unnecessary columns and rows
    # created by pandas module
    result.to_csv(outputfile)
    result = outputfile

    set_num = 1 # sets of files

    result = format_combined(result, set_num) # formatting
    csv_writer(result,outputfile) # writing formatted data to file


    # If there are more files to combine
    if len(oxyfiles) and len(deoxyfiles) != 0:
        # get oxy and deoxy files, format, create data frames
        third_set = oxyfiles.pop(0)
        third_set = format_file(third_set)

        second_oxy_set = pd.DataFrame(third_set)

        fourth_set = deoxyfiles.pop(0)
        fourth_set = format_file(fourth_set)

        second_deoxy_set = pd.DataFrame(fourth_set)

        # combine oxy data frames
        combineoxy = pd.concat([first_oxy_set,second_oxy_set], axis=1)

        # combine deoxy data frames
        combinedeoxy = pd.concat([first_deoxy_set,second_deoxy_set], axis=1)

        # combine oxy and deoxy data frames
        combinedresult = pd.concat([combineoxy,combinedeoxy], axis=1)
        combinedresult.to_csv(outputfile)
        combinedresult = outputfile

        set_num = 2 # sets of files

        combinedresult = format_combined(combinedresult, set_num) # formatting
        csv_writer(combinedresult,outputfile) # write formatted data to file


def format_file(filename):
    num_cols = 0 # columns
    data_file = csv.reader(open(filename, 'rb')) # open file

    rows1 = []
    # Append all file data to list
    for row in data_file:
        rows1.append(row)

    # Get length of file
    length = len(rows1)
    rows2 = []

    # Remove the first 39 rows
    for i in range(39):
        rows1.pop(0)

    # Look at second row, which is list of labels, and check for channels
    for col in rows1[1]:
        if 'CH' in col:
            num_cols += 1

    # Append remaining data minus the first column
    for i in range(length - 39):
        rows2.append(rows1[i][1:num_cols+1])
    return rows2

def format_combined(filename, set_num):
    data_file = csv.reader(open(filename, 'rb')) # open file

    # Append all file data to list
    rows1 = []
    for row in data_file:
        rows1.append(row)

    # Get length of file
    length = len(rows1)
    rows2 = []

    # Remove the first row
    for i in range(1):
        rows1.pop(0)

    # Changing headers for the set with 2 oxy and 2 deoxy files
    if set_num == 2:
        # Change first header
        rows1[0][1] = 'Probe 1 and Probe 2 oxy'

        # Change second header by finding and replacing 
        rows1[0] = [x.replace('Probe 1 deoxy', 'Probe 1 and Probe 2 deoxy') 
        for x in rows1[0]]

        # Count number of total oxy channels first by incrementing until the
        # deoxy label is reached. Once number of oxy channels are found, deoxy
        # channel number can be found by subtracting length of row from oxy_chan
        # Lastly, go through row one more time and change channel numbers
        oxy_chans = 0
        deoxy_chans = 0
        y = 0
        while 'deoxy' not in rows1[0][y]: # count number of oxy channels
            y += 1
            oxy_chans += 1

        deoxy_chans = (len(rows1[0]) - oxy_chans) # get deoxy channels

        for ox in range(oxy_chans):
            rows1[1][ox] = 'CH'+str(ox)

        for de in range(deoxy_chans):
            rows1[1][oxy_chans + de] = 'CH'+str(de+1) # add one for starting at 0

    # Append remaining data minus the first column
    for i in range(length - 1):
        rows2.append(rows1[i][1:])
    return rows2

def csv_writer(data, path):
    with open(path, "wb") as csv_file: # open file
        writer = csv.writer(csv_file, delimiter=',') # data seperated by commas
        for line in data:
            writer.writerow(line) # write each row of data to file

def main():
    combine()

main()