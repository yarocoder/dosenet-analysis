"""
# Module 4- Example Plot of Weather Data
#### author: Radley Rigonan

In this module, I will be desmonstrating a few other graphical capabilities in Python.
I will be using the following link to create a table and pi chart:
https://radwatch.berkeley.edu/sites/default/files/pictures/rooftop_tmp/weather.csv
"""
import csv
import io
import urllib.request            
import matplotlib.pyplot as plt
from datetime import datetime
import numpy as np      # This is the first time I have used numpy.
                        # numpy is a fundamental extension of python that enables usage of data arrays (among many, many other functions)

url = 'https://radwatch.berkeley.edu/sites/default/files/pictures/rooftop_tmp/weather.csv' 
response = urllib.request.urlopen(url)
reader = csv.reader(io.TextIOWrapper(response)) 
timedata = []
Bi214 = []
K40 = []
Cs134 = []
Cs137 = []
line = 0

for row in reader:
    if line != 0:
        timedata.append(datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S'))
        Bi214.append(float(row[1]))
        K40.append(float(row[2]))
        Cs134.append(float(row[3]))
        Cs137.append(float(row[4]))
    line += 1
    
def table():
    # For this table, we will have 4 rows with each isotope and
    # 5 columns with the following information: isotope,
    # mean CPM, median CPM, max CPM measured, and time of occurrence:
    RowLabel = ("Bi-214", "K-40", "Cs-134", "Cs-137")
    ColLabel = ("isotope", "mean concentration", "median concentration", "max concentration", "time of occurrence")    
    
    # Thus, the first step is to find each column of information
    # The statistical meaning of mean and a computational method to obtain it are explored in a different module.
    # For this module, we will use the Python command 'mean'
    mean_data = (mean(Bi214), mean(K40), mean(Cs134), mean(Cs137))
    
    # For median, we will use the Python command 'median'
    median_data = (median(Bi214), median(K40), median(Cs134), median(Cs137))
    
    # Python also has a function to scan a list for the max value contained in that list!
    max_data = (max(Bi214), max(K40), max(Cs134), max(Cs137))
    
    # The corresponding times for each maximum have matching datetime component with the same index.
    # I will use LIST.index(max(LIST)) to find these corresponding indices.  Note: this method's
    # weakness is that it only identifies the first occurrence of a maximum; if there the max occurs multiple times
    # it will not acknowledge them.  Can you think/find a way to do this in a better way?
    time_data = (timedata[Bi214.index(max(Bi214))], timedata[K40.index(max(K40))], 
                 timedata[Cs134.index(max(Cs134))], timedata[Cs137.index(max(Cs137))])       
    # Finally, put the data all together in a table!
                 
    data_array = np.vstack((RowLabel,mean_data,median_data, max_data,time_data)).T
    fig, ax = plt.subplots() 
    ax.axis('off') 
    ax.table(cellText=data_array, colLabels=ColLabel, loc='center')
    plt.show()
    
def pie_chart():
    # Let's create a pi chart that shows the breakdown of which isotope is measured to have the highest concentration
    # The following is an iterative script that tallies which isotope has the highest concentration measurement at each index:
    tally = [0,0,0,0]
    for i in range(0,len(Bi214)):
        comparing_list = [Bi214[i],K40[i], Cs134[i], Cs137[i]]
        if max(comparing_list) == Bi214[i]:
            tally[0] += 1
        elif max(comparing_list) == K40[i]:
            tally[1] += 1
        elif max(comparing_list) == Cs134[i]:
            tally[2] += 1
        else:
            tally[3] += 1
    
    labels = "Bi-214", "K-40", "Cs-134", "Cs-137"
    total_counts = sum(tally)
    fracs = [tally[0]/total_counts, tally[1]/total_counts, tally[2]/total_counts, tally[3]/total_counts]
    explode = (0,0,0,0)
    plt.pie(fracs, explode=explode, labels=labels) 
    plt.axis('equal')
    
    plt.show()
    