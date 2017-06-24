# -*- coding: utf-8 -*-

# Brian Plimley, 2016-09-08
# Tools for analyzing and plotting DoseNet data.

from __future__ import print_function
import requests
import csv
import numpy as np
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt

epoch_time = datetime(1970, 1, 1)


def get_dosenet_csv_data(nickname):
    """
    Get a CSV file from the RadWatch website.

    Input: nickname of DoseNet station.
    """

    if nickname[-4:] == '.csv':
        nickname = nickname[:-4]
    urlbase = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/'
    url = urlbase + '{}.csv'.format(nickname)

    req = requests.get(url)
    assert req.ok, 'Bad request. Is the nickname a public station?'
    f = req.iter_lines()

    ts, cpm, cpm_err = parse_csv_object(f)

    return ts, cpm, cpm_err


def parse_csv_object(filelike_object):

    # TODO: do this all with pandas in like 1 line
    reader = csv.DictReader(filelike_object)

    time_format = '%Y-%m-%d %H:%M:%S'

    ts = np.array([], dtype=float)
    cpm = np.array([], dtype=float)
    cpm_err = np.array([], dtype=float)

    for row in reader:
        this_datetime = datetime.strptime(row['receiveTime'], time_format)
        ts = np.append(ts, (this_datetime - epoch_time).total_seconds())
        cpm = np.append(cpm, float(row['cpm']))
        cpm_err = np.append(cpm_err, float(row['cpmError']))

    return ts, cpm, cpm_err


def parse_csv_file(filepath):
    """
    Take a local CSV file and parse into timestamp, cpm, cpm_error.
    """

    with open(filepath) as f:
        ts, cpm, cpm_err = parse_csv_object(f)

    return ts, cpm, cpm_err


def plot(ts, cpm, cpm_err, **kwargs):
    """
    Plot the data from a station, nicely.
    """

    datetimes = np.array([epoch_time + timedelta(seconds=s) for s in ts])

    plt.figure()
    plt.errorbar(datetimes, cpm, yerr=cpm_err, fmt='.b', **kwargs)


def check_data_reliability(ts):
    """
    Go through timestamp vector and check intervals.
    """

    dt = ts[1:] - ts[:-1]

    min_interval = 290
    max_interval = 310

    too_short = np.nonzero(dt < min_interval)[0]
    too_long = np.nonzero(dt > max_interval)[0]

    # import ipdb; ipdb.set_trace()
    for i in too_short:
        print('Too short: {} to {} ({} s)'.format(
            epoch_time + timedelta(seconds=ts[i]),
            epoch_time + timedelta(seconds=ts[i+1]),
            dt[i]))
    for i in too_long:
        print('Too long: {} to {} ({} s)'.format(
            epoch_time + timedelta(seconds=ts[i]),
            epoch_time + timedelta(seconds=ts[i+1]),
            dt[i]))
