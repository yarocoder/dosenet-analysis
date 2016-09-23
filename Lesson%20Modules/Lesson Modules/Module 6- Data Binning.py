"""
####Module 6- Data Binning

"""
import csv
import io
import urllib.request            
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime 

url = 'http://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof.csv' 
response = urllib.request.urlopen(url)
reader = csv.reader(io.TextIOWrapper(response)) 
timedata = []
counts = []
CPMerror = []
line = 0

for row in reader:
    if line != 0:
        timedata.append(datetime.fromtimestamp(float(row[2],)))
            # 3rd column if CSV is a UNIX timestamp that can be converted to datetime via fromtimestamp
        counts.append(float(row[6]))
        CPMerror.append(float(row[7]))
    line += 1

def month_bin():
    Year = [timedata[-1].year]
    Month = [timedata[-1].month]
    sumCPM = [0]        
    sumError = [0]
    DataCount = [0]
    flag = 0
    for i in range(len(counts)-1,-1,-1):
        if Year[flag] == timedata[i].year:
            if Month[flag] == timedata[i].month:
                sumCPM[flag] += counts[i]
                sumError[flag] += CPMerror[i]
                DataCount[flag] += 1
            else:
                Year.append(timedata[i].year)
                Month.append(timedata[i].month)
                sumCPM.append(0)
                sumError.append(0)
                DataCount.append(0)
                flag += 1
        else:
            Year.append(timedata[i].year)
            Month.append(timedata[i].month)
            sumCPM.append(0)
            sumError.append(0)
            DataCount.append(0)
            flag += 1
    
    binnedCPM = np.array(sumCPM) / np.array(DataCount)
    binnedError = np.array(sumError) / np.array(DataCount)
    strDates = [str(m)+'-'+str(n) for m,n in zip(Month,Year)]
    binnedDates = []
    for i in range(0,len(Month)):
        binnedDates.append(datetime.strptime(strDates[i],'%m-%Y'))
        
    fig, ax = plt.subplots()
    ax.plot(binnedDates,binnedCPM, 'ro-')
    ax.errorbar(binnedDates,binnedCPM, yerr=binnedError, fmt='ro', ecolor='r')
    plt.xticks(rotation=30)
    plt.title('DoseNet: Time-Averaged CPM (Etcheverry Roof)')
    plt.xlabel('Date')
    plt.ylabel('Average CPM')