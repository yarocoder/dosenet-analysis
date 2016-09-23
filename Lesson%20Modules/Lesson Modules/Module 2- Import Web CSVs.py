"""
@author: Radley Rigonan
This is an example of reading and importing .CSV files from a direct download link (DDL).  DDLs are hyperlinks that point to a file that will immediately be downloaded by your internet browser.

In this module, I will be using lbl.csv which can be accessed from the following link.
http://radwatch.berkeley.edu/sites/default/files/dosenet/lbl.csv
"""
import csv
import io
    # The io module allows Python to deal with objects formatted as bytes. Web sources are usually formatted in HTTP/bytes, rendering it incompatible with default Python modules.
import urllib.request     #The urllib module provides an interface to fetch data from the Internet.
url = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/etch.csv' 

def printwebCSV():
    # The following lines will: access the DDL, makes the file compatible to Python, and prints the CSV.  Take note that only the first two lines are different from reading a .CSV from the local disk
    response = urllib.request.urlopen(url)  # This line will fail without internet access.
    csvfile = io.TextIOWrapper(response)
        # io.TextIOWrapper decodes HTTP data encodes the data as string objects that can be understood by Python    
    reader = csv.reader(csvfile)
    for row in reader:
        print(', '.join(row))
        
def importwebCSV():
    # This module is an example of importing a CSV from a DDL.  It also uses more compact syntax in order to reduce the number of lines:
    response = urllib.request.urlopen(url)
    reader = csv.reader(io.TextIOWrapper(response))  
    datetime = []    
    cpm = []
    line = 0
    for row in reader:
        if line != 0:
            datetime.append(row[0])
            cpm.append(float(row[6]))
        line += 1    # Python syntax for line = line + 1 (+1 to current stored value for line)
    print(datetime,cpm)
    # This example typifies the overwhelming amount of data that you can handle with Python!  In only a few seconds, this script can record over 60,000 data points in your computer's memory.