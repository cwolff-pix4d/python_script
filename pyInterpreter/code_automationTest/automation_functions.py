import Pix4Dmatic
import os
from datetime import datetime
import platform



def run_project(project_name, project_path, img_path,  gcps_path, info_file, comment):
    """to process one project, gather info in a file"""
    """
    INPUT : 
        name = name of the project to be created
        project_path = path where project is created
        img_path = path to folder with the imgs to add
        info_path = path to the file where the info about processing will be written 
        gcps_path = path to file with gcps
    """


    info_file.write("************************\n")
    info_file.write(project_name + "\n")
    info_file.write(f"note :        {(comment)}\n")

    ### add gcps and imgs ###
    app = session()
    project = app.new_project(project_path, project_name)
    cluster = project.cluster_at(0)
    cluster.add_images_from(img_path).wait()
    if gcps_path != "N":
        cluster.add_gcps_from(gcps_path).wait()
    project.save()
    project.close()

    if platform.system() == "Windows":
        path_open = project_path + "\\" + project_name + "\\" + "root.p4a"
        path_cloud = project_path + "\\" + project_name + "\\" + project_name

    else:
        path_open = project_path + "/" + project_name + "/" + "root.p4a"
        path_cloud = project_path + "/" + project_name + "/" + project_name

    ### reconstruction ###
    project = app.open_project(path_open)
    time1 = datetime.now()
    cluster = project.cluster_at(0)
    cluster.reconstruct().wait()
    time2 = datetime.now()
    reconstruction_time = time2 - time1

    reconstruction = cluster.reconstruction
    metrics = reconstruction.metrics

    info_file.write(f'Calibrated cameras                          : {(reconstruction.metrics.calibrated_cameras_count)} / {len(cluster.input_cameras)}\n')
    info_file.write(f'points_gsd                                  : {(metrics.points_gsd)}\n ')
    info_file.write(f'median_tracks_count_per_camera              : {(metrics.median_tracks_count_per_camera)}\n ')
    info_file.write(
        f'mean_relative_difference_sensor_parameters  : {(metrics.mean_relative_difference_sensor_parameters)}\n ')

    for index in range(0, metrics.calibrated_cameras_count):
        info_file.write(f'track count for camera  {(index)} : {(metrics.track_count(index))}\n ')

    for index1 in range(0, metrics.calibrated_cameras_count):
        for index2 in range(0, metrics.calibrated_cameras_count):
            info_file.write(
                f'track count for camera  pair ({(index1)},{(index2)}) : {(metrics.track_count(index1, index2))} ')

    project.save()
    project.close()

    ### densify ###
    project = app.open_project(path_open)
    time3 = datetime.now()
    cluster = project.cluster_at(0)
    cluster.densify().wait()

    time4 = datetime.now()
    densify_time = time4 - time3
    project.save()
    project.close()

    ### export cloud ###
    project = app.open_project(path_open)
    cluster = project.cluster_at(0)
    time5 = datetime.now()
    cluster.export_sparse_point_cloud(path_cloud + "_sparse").wait()
    time6 = datetime.now()
    cluster.export_dense_point_cloud(path_cloud + "_dense").wait()
    time7 = datetime.now()
    export_sparse_time = time6 - time5
    export_dense_time = time7 - time6
    project.save()
    project.close()


    info_file.write("\n------- TIME -------\nreconstruction time : " + str(reconstruction_time)
                    + "\ndensify time : " + str(densify_time)
                    + "\nexport sparse cloud time : " + str(export_sparse_time)
                    + "\nexport dense cloud time : " + str(export_dense_time)
                    + "\n\n\n")



    app.quit()


def run_projects_list(list_path, result_folder_path, result_file_path):
    """to process several projects listed in a list"""
    """
    INPUT : 
        list_path = path to a file with list of projects to process
        result_folder_path = path to folder where to process and save results
        result_file_path = path to file for writting info about the processing 
    """

    if not os.path.exists(result_folder_path):
        os.makedirs(result_folder_path)

    info_file = open(result_file_path, "a")
    info_file_name,info_file_extension = os.path.splitext(os.path.basename(result_file_path))

    info_file.write("Results for processing : " + info_file_name + "\n" + str(datetime.now()) + "\n\n\n")

    file_datasets = open(list_path, "r")
    dataset_list = file_datasets.readlines()
    for dataset in dataset_list:
        process = dataset.split(";")[0]
        project_name = dataset.split(";")[1]
        images_path = dataset.split(";")[2]
        gcps_path = dataset.split(";")[3]
        comment = dataset.split(";")[4]
        print(project_name)
        print(images_path)
        print(gcps_path)
        if process != "*":
            run_project(project_name, result_folder_path, images_path, gcps_path, info_file, comment)
    file_datasets.close()
    info_file.close()

###   MAIN
list_projects_to_process = r"C:\Users\cwolff\Desktop\WEEKLY_automation_pyInterp\codes\QA\cameras_small.txt"
folder_to_stock_project = r"C:\Users\cwolff\Desktop\WEEKLY_automation_pyInterp\codes\QA\test_camIntegration\190705"
file_info_processing = r"C:\Users\cwolff\Desktop\WEEKLY_automation_pyInterp\codes\QA\test_camIntegration\190705\computeFile2.txt"

run_projects_list(list_projects_to_process, folder_to_stock_project, file_info_processing)