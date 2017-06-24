import csv
import io

# Python 2 and 3: easiest option
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime
from datetime import timedelta
from matplotlib.dates import date2num

def weather_station_data_scrape(ID, date):
    '''
    Scrap weather data of given location and given period of time from websites

    Arguments:
        - ID is a string contains weather station ID
    	- date is a 1 by 3 string array: Month/Date/Year
    '''

    data_temp=[]
    str1 = 'https://www.wunderground.com/weatherstation/WXDailyHistory.asp?ID='
    str2 = '&day='
    str3 = '&month='
    str4 = '&year='
    str5 = '&graphspan=day&format=1'
    url = str1+ID+str2+str(date.day)+str3+str(date.month)\
          +str4+str(date.year)+str5
    response = urlopen(url)
    #cr = csv.reader(response)
    cr=csv.reader(io.TextIOWrapper(response))
    for row in cr:
        if len(row)<= 1: continue
        data_temp.append(row)

    #Stores data with correct data type (datetime/string/double)
    data = [[0 for i in range(len(data_temp[1][:])-3)] for j in range(len(data_temp))]

    for i in range(len(data_temp)):
        if i == 0:
            data[0][:]=data_temp[0][0:len(data_temp[i][:])-2]
        elif i > 0:
            data[i][0]=datetime.strptime(data_temp[i][0], '%Y-%m-%d %H:%M:%S')
            data[i][1:data_temp[0][:].index('WindDirection')]=tuple(float(list_item) for list_item in data_temp[i][1:data_temp[0][:].index('WindDirection')])
            data[i][data_temp[0][:].index('WindDirection')] = data_temp[i][data_temp[0][:].index('WindDirection')]
            data[i][data_temp[0][:].index('WindDirection')+1:data_temp[0][:].index('Conditions')] = tuple(float(list_item) for list_item in data_temp[i][data_temp[0][:].index('WindDirection')+1:data_temp[0][:].index('Conditions')])
            data[i][data_temp[0][:].index('Conditions'):data_temp[0][:].index('Clouds')+1] = data_temp[i][data_temp[0][:].index('Conditions'):data_temp[0][:].index('Clouds')+1]
            data[i][data_temp[0][:].index('Clouds')+1:len(data_temp[0][:])-2] = tuple(float(list_item) for list_item in data_temp[i][data_temp[0][:].index('Clouds')+1:len(data_temp[i][:])-3])

    #Select data for output array:
    #   (Date,Temperature, Pressure, Windspeed, Humidity,
    #    Hourly Precipitation, and Solar radiation)
    data_out = [[0 for i in range(7)] for j in range(len(data))]

    for i in range(len(data_temp)):
        data_out[i][0:2] = data[i][0:2]
        data_out[i][2] = data[i][3]
        data_out[i][3] = data[i][6]
        data_out[i][4:6] = data[i][8:10]
        data_out[i][6] = data[i][12]

    # remove meta data
    data_out.pop(0)
    return data_out
