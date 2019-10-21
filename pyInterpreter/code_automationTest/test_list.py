
import os
from datetime import datetime
from parameters_cameras import *





def read_projects(path):

    """path = [app_to_run, list_projects_to_process, folder_to_stock_project, file_info_processing, py_test_case]"""

    app_to_run = path[0]
    list_projects_to_process = path[1]
    folder_to_stock_project = path[2]
    file_info_processing = path[3]
    py_test_case = path[4]

    if os.path.exists(folder_to_stock_project):
        os.remove(folder_to_stock_project)
    if not os.path.exists(folder_to_stock_project):
        os.makedirs(folder_to_stock_project)

    """info_file = open(file_info_processing, "w")
    info_file_name, info_file_extension = os.path.splitext(os.path.basename(file_info_processing))
    info_file.write("Results for processing : " + info_file_name + "\n" + str(datetime.now()) + "\n\n\n")
    info_file.close()"""

    file_datasets = open(list_projects_to_process, "r")
    dataset_list = file_datasets.readlines()
    for dataset in dataset_list:
        if dataset.split(";")[0]!= "*":
            os.environ["Dataset"] = dataset
            os.environ["Folder_to_stock_project"] = folder_to_stock_project
            os.environ["File_info_processing"] = file_info_processing
            cmd_line = app_to_run +" " + py_test_case
            print(os.environ["Dataset"])
            print(len(os.listdir(dataset.split(";")[2])))
            os.system(cmd_line)
    return 0


read_projects(path)


