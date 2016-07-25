
"""
@author: Radley Rigonan
This is an example of basic usage of matplotlib to create scatter plots, line graphs, and histograms.  These basic formats for data visualization are fundamental to displaying information in a clear and organized manner. The matplotlib website features a large collection of examples and documentation if you are interested in intermediate and advanced plotting.

In this module, I will be using etch.csv AND lbl.csv which can be accessed from the following links.
https://radwatch.berkeley.edu/sites/default/files/dosenet/etch.csv
http://radwatch.berkeley.edu/sites/default/files/dosenet/lbl.csv
"""
import csv
import io
import urllib.request            
import matplotlib.pyplot as plt    #matplotlib is one of the most commonly used Python extensions for plotting.  The plt identifier for matplotlib.pyplot is conventional practice in many codes.

# First we want to import two sets of data from DoseNet:
# You should recognize the following steps!  If you are not famiar with importing data from a DDL, then check previous modules on retrieving and importing CSVs.
url_etch = 'https://radwatch.berkeley.edu/sites/default/files/dosenet/etch.csv' 
response_etch = urllib.request.urlopen(url_etch)
reader_etch = csv.reader(io.TextIOWrapper(response_etch)) 
datetime_etch = []    
cpm_etch = []
line = 0
for row in reader_etch:
    if line != 0:
        datetime_etch.append(row[0])
        cpm_etch.append(float(row[1]))
    line += 1

url_lbl = 'http://radwatch.berkeley.edu/sites/default/files/dosenet/lbl.csv' 
response_lbl = urllib.request.urlopen(url_lbl)
reader_lbl = csv.reader(io.TextIOWrapper(response_lbl)) 
datetime_lbl = []    
cpm_lbl = []
line = 0
for row in reader_lbl:
    if line != 0:
        datetime_lbl.append(row[0])
        cpm_lbl.append(float(row[1]))
    line += 1

def line():
    # The following commands plot CPM on the y-axis against x=1 for the 1st point, x=2 for the 2nd point, etc..  It connects each point with a line, creating a line graph.
    plt.plot(cpm_etch)
    plt.ylabel('Counts Per Minute')                       # label the y-axis
    plt.title('DoseNet Measurements: Etcheverry Roof Line Graph')    # put a title!
    plt.show()                                            # matplotlib's equivalent of the print command
    
def scatter():
    # Alternatively, you can create a scatter plot by with a modifier in plt.plot's inputs. For more insight into line, axes, and other plot modifiers, see the next module.
    plt.plot(cpm_lbl,'ro')     # The modifier after cpm does two things: r changes the color to red and o creates points instead of lines
    plt.ylabel('Counts Per Minute')
    plt.title('DoseNet Measurements: Lawrence Berkeley Labs Scatter Plot')    
    plt.show()   

def histogram():
    # Histograms are a graphics that depict distributions of data.  They are incredibly useful in statistical analysis and can be created in a similar fashion as scatter plots, but with the hist command:
    plt.hist(cpm_etch,bins=100)
    plt.ylabel('Frequency')
    plt.xlabel('Counts Per Minute')
    plt.title('DoseNet Measurements: Etcheverry Roof Histogram')
    plt.show()
        
def subplot_overlay():
    # With subplots, multiple plots can be placed on a single canvas.  Likewise, there are also methods to place multiple sets of data on a single axis.
    plt.subplot(2,2,1)    # This means you are making a subplot with 2 rows, 2 columns, and are currently working on the 1st one (plot in top right)
    plt.plot(cpm_etch,'o')
    plt.ylabel('Counts Per Minute')
    plt.title('Etcheverry Roof Scatter Plot')
    
    plt.subplot(2,2,2)    # inputs signify 2 rows, 2 columns, 2nd plot
    plt.hist(cpm_lbl,bins=50)
    plt.ylabel('Frequency')
    plt.xlabel('Counts Per Minute')
    plt.title('LBL Histogram')

    plt.subplot(2,1,2)   # More complex example: 2 rows, 1 column, 2nd plot.  Thus, this plot will be the width of both the plots above it.
    plot1, = plt.plot(cpm_lbl,'c')      
    plot2, = plt.plot(cpm_etch,'g')     # Note: The comma after naming the variable is necessary or plt.legend will fail
    plt.ylabel('Counts Per Minute')
    plt.title('DoseNet Measurements: Etcheverry Roof and Lawrence Berkeley Labs Scatter Plot')
    plt.legend([plot1, plot2], ['LBL', 'Etcheverry'])  # Giving the plots names enables us to label them in a legend!
    
    plt.show()

# This was a short rundown of matplotlib's capabilities.  If you are interested in creating a more professional plot, the next module will take a more in depth look at manipulating plots to create an optimal visual representation.