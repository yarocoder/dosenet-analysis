import csv
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.path as path
import matplotlib.dates as mdates
from dateutil.parser import parse
from datetime import datetime
from datetime import timedelta
import urllib2
import pytz
from matplotlib.backends.backend_pdf import PdfPages
from scipy import optimize
from scipy import asarray as ar,exp
from scipy.integrate import quad

def lbound(bound,par):
    return 1e4*np.sqrt(bound-par) + 1e-3*(bound-par) if (par<bound) else 0

def ubound(bound,par):
    return 1e4*np.sqrt(par-bound) + 1e-3*(par-bound) if (par>bound) else 0

def bound(bounds,par):
    return lbound(bounds[0],par) + ubound(bounds[1],par)

def fixed(fix,par):
    return bound((fix,fix), par)

def gaus(x,a,x0,sigma):
    return a*exp(-(x-x0)**2/(2*sigma**2))+lbound(0,a)+lbound(0,sigma)+lbound(0,x0)

def expo(x,a,slope):
    return a*exp(x*slope)

# p = [a1,mean,sigma,a2,shift,slope,const]
def gaus_plus_exp(x,p):
    return gaus(x,p[0],p[1],p[2])+expo(x,p[3],p[4])

# p = [a1,mean,sigma,slope,const]
def gaus_plus_line(x,p):
    return gaus(x,p[0],p[1],p[2])+p[3]*x+p[4]

def double_gaus_plus_exp(x,p):
    return gaus(x,p[0],p[1],p[2])+gaus(x,p[3],p[4],p[5])+expo(x,p[6],p[7])

def double_gaus_plus_line(x,p):
    return gaus(x,p[0],p[1],p[2])+gaus(x,p[3],p[4],p[5])+p[6]*x+p[7]

def make_int(lst): 
    '''
    Makes all entries of a list an integer
    '''
    y = []
    for i in lst:
        y.append(int(i))
    return y

def make_array(lst): 
    '''
    Makes list into an array. Also splices out the irrelevant stuff 
    for a spectra
    '''
    y = np.asarray(make_int(lst[12:]))
    return y

def get_times(rows, number, n=1):
    entries = 12*n
    days = (24/n)
    i = 0
    counter = 0
    times = []
    while i < number*days:
        if counter < days:
            time_range = []
            integration = rows[(i*entries)+1:((i+1)*entries)+1]
            for j in integration:
                time_range.append(parse(j[1]))
            times.append(time_range[int(len(time_range)/2)])
            counter+=1
            i+=1
        else:
            print('finished', i)
            counter = 0

    print('finished', i)
    counter = 0
    return times

def double_peak_finder(array,lower,upper):
    points = ar(range(lower,upper))
    peak = list(array[lower:upper])
    counts = ar(peak)

    nentries = len(points)
    mean = lower + (upper - lower)/2.0
    slope = 2*(np.log(counts[-1])-np.log(counts[0]))/(points[-1]-points[0])
    pinit = [counts[0]/5.0,mean-2,5.0,counts[0]/5.0,mean+2,5.0,counts[0],slope]

    errfunc = lambda p, x, y: double_gaus_plus_exp(x,p) - y 
    pfit,pcov,infodict,errmsg,success = \
        optimize.leastsq(errfunc, pinit, args=(points,counts), \
            full_output=1, epsfcn=0.0001)

    if (len(counts) > len(pinit)) and pcov is not None:
        s_sq = (errfunc(pfit, points, counts)**2).sum()/(len(counts)-len(pinit))
        pcov = pcov * s_sq
    else:
        pcov = 0

    error = [] 
    for i in range(len(pfit)):
        try:
          if np.absolute(pcov[i][i])**0.5 > np.absolute(pfit[i]):
            error.append( 0.00 )
          else:
            error.append(np.absolute(pcov[i][i])**0.5)
        except:
          error.append( 0.00 )
    pfit_leastsq = pfit
    perr_leastsq = np.array(error) 
    return pfit_leastsq, perr_leastsq 

def peak_finder(array,lower,upper,count_offset): 
    '''
    Peak Finder for Potassium. Needs more development
    '''
    points = ar(range(lower,upper))
    peak = list(array[lower:upper])
    counts = ar(peak)

    nentries = len(points)
    mean = lower + (upper - lower)/2.0
    slope = 2*(np.log(counts[-1])-np.log(counts[0]))/(points[-1]-points[0])
    pinit = [counts[0]/2.0,mean,5.0,counts[0]*count_offset,slope]

    errfunc = lambda p, x, y: gaus_plus_exp(x,p) - y 
    pfit,pcov,infodict,errmsg,success = \
        optimize.leastsq(errfunc, pinit, args=(points,counts), \
            full_output=1, epsfcn=0.0001)

    if (len(counts) > len(pinit)) and pcov is not None:
        s_sq = (errfunc(pfit, points, counts)**2).sum()/(len(counts)-len(pinit))
        pcov = pcov * s_sq
    else:
        pcov = 0

    error = [] 
    for i in range(len(pfit)):
        try:
          error.append(np.absolute(pcov[i][i])**0.5)
        except:
          error.append( 0.00 )
    pfit_leastsq = pfit
    perr_leastsq = np.array(error) 
    return pfit_leastsq, perr_leastsq 

def get_double_peaks(rows, number, n=1, lower_limit=240, upper_limit=300, make_plot = False):
    entries = 12*n
    days = (24/n)
    i = 0
    counter = 0
    means = []
    sigmas = []
    amps = []
    while i < number*days:
        if counter < days:
            integration = rows[(i*entries)+1:((i+1)*entries)+1]
            array_lst = [] 
            for j in integration:
                array_lst.append(make_array(j))

            integrated = sum(array_lst)
            #print integrated
            fit_pars, fit_errs = double_peak_finder(integrated,lower_limit,upper_limit)
            mean = [fit_pars[1],fit_errs[1]]
            sigma = [fit_pars[2],fit_errs[2]]
            amp = [fit_pars[0],fit_errs[0]]
            if fit_pars[4] > fit_pars[1]:
                mean = [fit_pars[4],fit_errs[4]]
                sigma = [fit_pars[5],fit_errs[5]]
                amp = [fit_pars[3],fit_errs[3]]
            means.append(mean)
            sigmas.append(sigma)
            amps.append(amp)

            counter+=1 
            i+=1
            if make_plot:
                fig = plt.figure()
                fig.patch.set_facecolor('white')
                plt.title('Spectra integrated over a day')
                plt.xlabel('channels')
                plt.ylabel('counts')
                plt.xlim(1,500)
                x = ar(range(0,len(integrated)))
                plt.plot(x,integrated,'b:',label='data')
                plt.plot(x,double_gaus_plus_exp(x,fit_pars),'ro:',label='fit')
                plt.legend()
                plt.yscale('log')
                plt.show()
        else:
            counter = 0
    counter = 0

    return means, sigmas, amps

def get_peaks(rows, number=1, n=1, lower_limit=240, upper_limit=300, make_plot = False,count_offset=100): 
    '''
    Gets single gaussian peaks in the specified window
    number is the number of days of spectras to go through
    n is the number of hours that each spectra is integrated over 
    lower_limit, upper_limit set the window to look for a peak inside
    '''
    entries = 12*n
    days = (24/n)
    print('making {} plots for each day'.format(days))
    i = 0
    counter = 0
    means = []
    sigmas = []
    amps = []
    while i < number*days:
        if counter < days:
            integration = rows[(i*entries)+1:((i+1)*entries)+1]
            array_lst = [] 
            for j in integration:
                array_lst.append(make_array(j))

            integrated = sum(array_lst)
            #print integrated
            fit_pars,fit_errs = peak_finder(integrated,lower_limit,upper_limit,count_offset)
            means.append([fit_pars[1],fit_errs[1]])
            sigmas.append([fit_pars[2],fit_errs[2]])
            amps.append([fit_pars[0],fit_errs[0]])

            counter +=1 
            i+=1
            if make_plot:
                fig = plt.figure()
                fig.patch.set_facecolor('white')
                plt.title('Spectra integrated over a day')
                plt.xlabel('channels')
                plt.ylabel('counts')
                plt.xlim(1,500)
                #plt.ylim()
                x = ar(range(0,len(integrated)))
                plt.plot(x,integrated,'b:',label='data')
                plt.plot(x,gaus_plus_exp(x,fit_pars),'ro:',label='fit')
                plt.legend()
                plt.yscale('log')
                plt.show()
        else:
            counter = 0
    counter = 0
    return means,sigmas,amps

def get_mean(values):
    mean = 0
    var = 0
    for i in range(len(values)):
        if values[i] > 1:
            mean += values[i]
    mean = mean/len(values)
    for i in range(len(values)):
        if values[i] > 1:
            var += (mean - values[i])**2
    np.sum(values)/len(values)
    var = np.sqrt(var/len(values))
    return mean, var

def get_peak_counts(means,sigmas,amps):
    counts = []
    for i in range(len(means)):
        count,err = quad(gaus,0,500,args=(amps[i],means[i],sigmas[i]))
        counts.append(count)
    return counts

def get_calibration(rows,ndays):
    Bi_peaks, Bi_sigmas, Bi_amps = get_double_peaks(rows,ndays,24,80,160,True)
    K_peaks,K_errs = get_peaks(rows,ndays,24,220,320)

    print(Bi_peaks)
    print(K_peaks)

    Bi_mean, Bi_var = get_mean(np.asarray(Bi_peaks))
    K_mean, K_var = get_mean(np.asarray(K_peaks))
    print('bizmuth peak channel = {}, potassium peak channel = {}'.format(Bi_mean,K_mean))

    calibration_constant = (1460-609)/(K_mean - Bi_mean)
    print('keV/channel = {}'.format(calibration_constant))
    return calibration_constant

if __name__ == '__main__':
	# import data from weather station for all isotopes
    date = []
    cpm = []
    cpm_error = []
    line = 0
    url = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/lbl_outside_d3s.csv'
    #url = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/etch_roof_d3s.csv'
    print(url)
    response = urllib2.urlopen(url)
    print(response)
    rows = []
    reader = csv.reader(response, delimiter=",")

    for row in reader:
        rows.append(row)
    #    if line > 0:
    #        date.append(parse(row[1]))
    #        cpm.append(float(row[3]))
    #        cpm_error.append(float(row[4]))
    #    line += 1
    #print 'collected data between ', date[0], ' and ', date[-1]

    #get_calibration(rows,5)

    ndays = 2
    nhours = 1
    times = get_times(rows,ndays,nhours)
    K_peaks, K_sigmas, K_amps = get_peaks(rows,ndays,nhours,220,320)
    K_ch = np.asarray([i[0] for i in K_peaks])
    K_ch_errs = np.asarray([i[1] for i in K_peaks])
    K_sig = [i[0] for i in K_sigmas]
    K_A = [i[0] for i in K_amps]
    K_counts = get_peak_counts(K_ch,K_sig,K_A)

    Bi_peaks,Bi_sigmas,Bi_amps = get_double_peaks(rows,ndays,nhours,80,160)
    #Bi_peaks,Bi_sigmas,Bi_amps = get_peaks(rows,ndays,nhours,82,162,False,1)
    Bi_ch = np.asarray([i[0] for i in Bi_peaks])
    Bi_ch_errs = np.asarray([i[1] for i in Bi_peaks])
    Bi_sig = [i[0] for i in Bi_sigmas]
    Bi_A = [i[0] for i in Bi_amps]
    Bi_counts = get_peak_counts(Bi_ch,Bi_sig,Bi_A)

    calibs = (1460-609)/(K_ch - Bi_ch)
    calib_err = (1460-609)/(K_ch - Bi_ch)**2 \
        *np.sqrt(Bi_ch_errs**2 + K_ch_errs**2)

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    plt.title('K-40 counts vs Time')
    plt.xlabel('Time')
    plt.ylabel('counts')
    ax.plot(times,K_counts, 'ro')
    ax.errorbar(times,K_counts,yerr=np.sqrt(K_counts),fmt='ro',ecolor='r')
    plt.show()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    plt.title('Bi-214 counts vs Time')
    plt.xlabel('Time')
    plt.ylabel('counts')
    ax.plot(times,Bi_counts, 'ro')
    ax.errorbar(times,Bi_counts,yerr=np.sqrt(Bi_counts),fmt='ro',ecolor='r')
    plt.show()

    Bi_mean, Bi_var = get_mean(np.asarray(Bi_counts))
    print('Bi-214 <N> = {} +/- {}'.format(Bi_mean,Bi_var))

    K_mean, K_var = get_mean(np.asarray(K_counts))
    print('K-40 <N> = {} +/- {}'.format(K_mean,K_var))

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    plt.title('1460 Center channel vs Time')
    plt.xlabel('Time')
    plt.ylabel('1460 center channel')
    ax.plot(times,K_ch, 'ro')
    ax.errorbar(times,K_ch,yerr=K_ch_errs,fmt='ro',ecolor='r')
    plt.show()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    plt.title('609 Center channel vs Time')
    plt.xlabel('Time')
    plt.ylabel('609 center channel')
    ax.plot(times,Bi_ch, 'ro')
    ax.errorbar(times,Bi_ch,yerr=Bi_ch_errs,fmt='ro',ecolor='r')
    plt.show()

    fig, ax = plt.subplots()
    fig.patch.set_facecolor('white')
    plt.title('keV/channel vs Time')
    plt.xlabel('Time')
    plt.ylabel('keV/channel')
    #plt.ylim(4.9,5.15)
    plt.ylim(5.6,6.0)
    ax.plot(times,calibs, 'bo')
    ax.errorbar(times,calibs,yerr=calib_err,fmt='bo',ecolor='b')
    plt.show()

