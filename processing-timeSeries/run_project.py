import Pix4Dmatic
import os
from datetime import datetime
import platform
import sys
import shutil

def time_processing(projectPath, imagePath, timeSerie):
    app = session()
    projectName = "PROJ"
    project = app.new_project(projectPath, projectName)
    cluster = project.cluster_at(0)

    #1- add images
    time0 = datetime.now()
    cluster.add_images_from(imagePath).wait()
    project.save()
    time1 = datetime.now()
    add_time = time1 - time0

    #2- calibration
    cluster.reconstruct().wait()
    time2 = datetime.now()
    reconstruction_time = time2 - time1
    project.save()

    #3- dense
    cluster.densify().wait()
    time3 = datetime.now()
    dense_time = time3 - time2
    project.save()
    project.close()

    #files
    shutil.rmtree(os.path.join(projectPath, projectName))
    timeFile = open(timeSerie, "a")
    time = datetime.now().date().strftime('%y%m%d')
    string =       str(time + ";"
                 + str(add_time.total_seconds()) + ";"
                 + str(reconstruction_time.total_seconds()) + ";"
                 + str(dense_time.total_seconds()) + "\n")
    print(string)
    timeFile.write(string)
    timeFile.close()
    return 0

def time_AddImages(projectPath, imagePath, timeSerie):
    app = session()
    projectName = "PROJ"
    project = app.new_project(projectPath, projectName)
    cluster = project.cluster_at(0)

    #1- add images
    time0 = datetime.now()
    cluster.add_images_from(imagePath).wait()
    project.save()
    time1 = datetime.now()
    add_time = time1 - time0

    # files
    shutil.rmtree(os.path.join(projectPath, projectName))
    timeFile = open(timeSerie, "a")
    time = datetime.now().date().strftime('%y%m%d')
    string = str(time + ";" + str(add_time.total_seconds()) + "\n")
    timeFile.write(string)
    timeFile.close()

    return 0



####  MAIN

if platform.system() == "Windows":
    timeSerie_process = "CHANGES/time_process_win.txt"
    timeSerie_add = "CHANGES/time_add_win.txt"

    projectPath = "CHANGES"

    imagePath_process = "CHANGES_10images"
    imagePath_Add = "CHANGES_10images"

else:
    timeSerie_process = "/Users/cwolff/Desktop/python_script/processing-timeSeries/time_process_mac.txt"
    timeSerie_add = "/Users/cwolff/Desktop/python_script/processing-timeSeries/time_add_mac.txt"

    projectPath = "/Users/cwolff/Desktop/python_script/processing-timeSeries"

    imagePath_process = "/Users/cwolff/Desktop/python_script/processing-timeSeries/10images"
    imagePath_Add = "/Users/cwolff/Desktop/python_script/processing-timeSeries/10images"

time_processing(projectPath, imagePath_process, timeSerie_add)

