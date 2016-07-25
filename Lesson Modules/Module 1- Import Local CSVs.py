"""
@author: Radley Rigonan
This is an example of reading and importing .CSV files stored in your device onto Python.  Comma separated values (.CSV) is a filetype that stores tabular data in plaintext. It is a  widely standard format used in spreadsheets, data storage, and data exchange.

In this module, I will be using lbl.csv which can be downloaded from the following link:
http://radwatch.berkeley.edu/sites/default/files/dosenet/lbl.csv
"""
import csv      # module used for reading and converting .CSV files
import os       # module that enables local operating system dependent commands

# Normally, you're file of interest is not located in the default working directory of Python. os.chdir() changes the working directory so we can open our file of interest.
filepath = 'C:/Users/Radley/Downloads' # save file location as a string.
os.chdir(filepath)                     # and use os.chdir() to change the directory
filename = 'lbl.csv'                   # now that you are in the correct directory, store the file name
csvfile = open(filename)               # finally, open the file with Python

def printlocalCSV():
    # The following commands will: read the .CSV with csv.reader and display the data in your console one row at a time. This display command inserts a comma and space between each data entry, effectively reprinting the .CSV in your Python console.
    reader = csv.reader(csvfile)
    for row in reader:
        print(', '.join(row))

def importlocalCSV():
    # This module is an example of reading the .CSV and importing the data as variables in Python.  In many circumstances, you will want to import the data so that it can be used in Python.  In addition, I use csv.reader with different, more efficient syntax:    
    datetime = []               # set up an empty list so you can place the data into it.
    cpm = []
    line = 0                    # we want to ignore the 1st row of headers, so we set a variable to count the row we are iterating on.
    with open(filename) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if line != 0:       # if-statement to ignore first row of headers
                datetime.append(row[0])     # append means ATTACH.  We are attaching data in the 1st column to our list, row by row
                cpm.append(row[1])          # and repeat for the 2nd column
            line += 1
    print(datetime,cpm)
