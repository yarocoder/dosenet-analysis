import csv
import io
import urllib.request
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import timedelta
from matplotlib.dates import date2num

def findNearestDate(alist,date,delta):
    #Binary search to find the nearest datetime within tolerance in a list given a specific date
    #Delta is the tolerance
    
    midpoint = (len(alist)-1)//2 
    
    if midpoint < 0:
        return None
    else:
        if abs(alist[midpoint]-date) < delta:
                return alist[midpoint]
        else:
                if date < alist[midpoint]:
                    return findNearestDate(alist[0:midpoint],date,delta)
                else:
                    return findNearestDate(alist[midpoint+1:],date,delta)
def mergeData(raw_date, CPM, date):
    #Merge radiation data to weather data; raw_date and CPM are from radiation data
    #Each time in date list is matched up with the nearest date in raw_date list
    
    delta = timedelta(minutes=5)
    merge = [0 for i in range(len(date))]

    for i in range (len(date)):
        new_date = findNearestDate(raw_date,date[i],delta)
        merge[i] = CPM[raw_date.index(new_date)]
            
 
    return merge
def calculateCorrelationCoefficient(data_x, data_y):
    # Correlation Coefficient:
    #r = sum((x(i)-x_avg)*(y(i)-y_avg))/sqrt( sum( (x(i)-x_avg)^2 )*sum( (y(i)-y_avg)^2 ) )
    #Variance = (standard deviation)^2
    sum_x = 0
    sum_y = 0
    sum_xy = 0
    x_var = 0
    y_var = 0
    x_avg = sum(data_x)/len(data_x)
    y_avg = sum(data_y)/len(data_y)

    for i in range(0,len(data_x)):
        sum_xy += (data_x[i]-x_avg) * (data_y[i]-y_avg)
        sum_x += (data_x[i]-x_avg)*(data_x[i]-x_avg)
        sum_y += (data_y[i]-y_avg)*(data_y[i]-y_avg)
    
    x_var = np.sqrt(sum_x/(len(data_x)-1))
    y_var = np.sqrt(sum_y/(len(data_y)-1))
    r = sum_xy/np.sqrt(sum_x*sum_y)
    return r, x_var, y_var,x_avg,y_avg