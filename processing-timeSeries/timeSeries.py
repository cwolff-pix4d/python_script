from pandas import read_csv
from matplotlib import pyplot
import platform

def timeGraph_Process(seriesFile):
    series = read_csv(seriesFile, sep=';')
    print(series)
    series.plot(y=['Calib_time','Dense_time'])
    pyplot.show()

    series.plot(y=['Add_time'])
    pyplot.show()
    return 0

def timeGraph_Add(seriesFile):
    series = read_csv(seriesFile, sep=';')
    print(series)
    series.plot(y=['Add_time'])
    pyplot.show()
    return 0




# MAIN
if platform.system() == "Windows":
    filePath_process = "TO BE CHANGED"
    filePath_add = "TO BE CHANGED"
else:
    filePath_process = "/Users/cwolff/Desktop/python_script/processing-timeSeries/time_process_mac.txt"
    filePath_add = "/Users/cwolff/Desktop/python_script/processing-timeSeries/time_add_mac.txt"

timeGraph_Process(filePath_process)
timeGraph_Add(filePath_add)