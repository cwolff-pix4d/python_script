#import Pix4Dmatic
import os
import shutil
from datetime import datetime
import platform
import numpy as np


def QA_bMERGE(project_name, project_path, img_path):
    app = session()
    #1
    project = app.new_project(project_path, project_name)
    cluster = project.cluster_at(0)
    cluster.add_images_from(img_path).wait()
    print("print")
    project.info("info")

    project.save()
    project.close()

    #2
    created_project = project_path + "\\" + project_name + "\\root.p4a"
    project = app.open_project(created_project)
    cluster = project.cluster_at(0)
    cluster.reconstruct().wait()
    project.save()
    print("1")
    project.close()

    #3
    project = app.open_project(created_project)
    cluster = project.cluster_at(0)
    cluster.densify().wait()
    project.save()
    print("2")
    project.close()

    #4
    project = app.open_project(created_project)
    cluster = project.cluster_at(0)
    cluster.export_sparse_point_cloud(project_path + "\\" + project_name + "\\sparse").wait()
    cluster.export_dense_point_cloud(project_path + "\\" + project_name + "\\dense").wait()
    project.save()
    return 1


project_name = str(datetime.now())[0:10] + "_" + str(datetime.now())[-5:-1]
print(project_name)
if platform.system() == "Wdindows":
    project_path = r"C:\Users\cwolff\Desktop\QA_bMERGE\results"
    img_path = r"C:\Users\cwolff\Desktop\QA_bMERGE\4imgs"
else:
    project_path = r"C:/Users/cwolff/Desktop/QA_bMERGE/results"
    img_path = r"C:/Users/cwolff/Desktop/QA_bMERGE/4imgs"

QA_bMERGE(project_name, project_path, img_path)
