# -*- coding: utf-8 -*-
"""
#### Module 7- Data Sorting and Searching

Computer scripts excel at performing repetetive tasks that would normally be tedious or uninteresting to do by hand.  Therer are many useful jobs that programs can perform, but in this module I will demonstrate three common data-processing techniques: sorting, searching, and manipulating.  These jobs are fundamental functions of computer scripts and are encountered in nearly any field of computational data analysis.

For this module I will be using AirMonitor's archived weather data from July 23 2015 to July 23 2016
https://www.wunderground.com/history/airport/KOAK/2015/7/23/CustomHistory.html?dayend=23&monthend=7&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1
"""
import csv
import io
import urllib.request            
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

url = 'https://www.wunderground.com/history/airport/KOAK/2015/7/23/CustomHistory.html?dayend=23&monthend=7&yearend=2016&req_city=&req_state=&req_statename=&reqdb.zip=&reqdb.magic=&reqdb.wmo=&format=1'
response= urllib.request.urlopen(url)
reader = csv.reader(io.TextIOWrapper(response)) 
datalist = []
timedata = []
meantemp = []    
meanwind = []
rain = []
line = 0

for row in reader:
    if line != 0:
        datalist.append(row)   # intermediate step of piling data into one list because url is a comma delimited url.
    line += 1
     
for i in range(len(datalist)):
    if i !=0:
        timedata.append(datetime.strptime(datalist[i][0], '%Y-%m-%d'))
        meantemp.append(float(datalist[i][2]))
        meanwind.append(float(datalist[i][17]))
        rain.append(datalist[i][19])
        
data = np.array((timedata,meantemp,meanwind,rain))
    # now all the data is gathered in a multidimensional array in which the 1st column has dates, 2nd column has mean temperature, 3rd column has mean wind velocity, and 4th column has precipitation data.

def sort_func(type):
    # INPUT: type is a string, either 'temp,'wind', or 'rain' to determine how how the list array is sorted
    if type == 'temp':
        sorted_index = np.argsort(data[1])     # argsort outputs a sorted list of indices from lowest to highest for the (1+1)nd row
        sorted_data = data[:,sorted_index]     # which is used to sort the columns in the multi-dimensional array
    elif type == 'wind':
        sorted_index = np.argsort(data[2])     # outputs a sorted list of indices from lowest to highest for the (1+2)rd row
        sorted_data = data[:,sorted_index]
    elif type == 'rain':
        sorted_index = np.argsort(data[3])     # outputs a sorted list of indices from lowest to highest for the (1+3)th row
        sorted_data = data[:,sorted_index]
    else:
        print('invalid input string')
    return sorted_data                      # module outputs the sorted_data

# Note, this sort function is not entirely correct.  When rainfall is detectable but not measurable, Wunderground stores the data as T for trace.  Thus, a proper sorting function for rain would be [0, ..., 0, T, ..., T, 0.1, ..., etc.]

def printed_sort():
    print(sort_func('temp')[1:,:9])
    print(sort_func('wind')[1:,:9])
    print(sort_func('rain')[1:,:9])

def search_func():
    # Let's make a function that searches for the dates in which rainfall is detected (including trace amounts of rainfall, 'T')
    # To do this, we can use a concept called list comprehension:
    rainfall = list(data[3:,].flatten())
    indices_trace = [i for i, target in enumerate(rainfall) if target == 'T']
    
    # Next, we replace indices where 'T' appears with 0 so it doesn't interfere with next search
    for index in indices_trace:
        rainfall[index] = 0
    
    rainfall = [float(j) for j in rainfall]
    indices_rain = [i for i, target in enumerate(rainfall) if target > 0]
    # When we combine the two indices, we place T before the numerical values
    search_index = indices_trace + indices_rain
    return search_index
    
    
def printed_search():
    search_index = search_func()
    print(data[:,search_index])
    
    

    