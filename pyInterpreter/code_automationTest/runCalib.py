import Pix4Dmatic
import os
from datetime import datetime
import platform
import sys



def test_case(dataset,folder_to_stock_project, file_info_processing):
    process = dataset.split(";")[0]
    project_name = dataset.split(";")[1]
    images_path = dataset.split(";")[2]
    gcps_path = dataset.split(";")[3]
    comment = dataset.split(";")[4]

    info_file = open(file_info_processing, "a")
    info_file.write("************************\n")
    info_file.write(project_name + "\n")
    info_file.write(f"note :        {(comment)}\n")

    ### add gcps and imgs ###
    app = session()
    project = app.new_project(folder_to_stock_project, project_name)
    cluster = project.cluster_at(0)
    time00 = datetime.now()
    cluster.add_images_from(images_path).wait()
    images = cluster.input_cameras
    if str(images.status) == "Status.Failed":
        info_file.write("error during the import of images : " + project_name + "\n")
        #app.quit()
        info_file.close()
        return False
    time01 = datetime.now()
    add_time = time01 - time00
    if gcps_path != "N":
        cluster.add_gcps_from(gcps_path).wait()
    project.save()
    #project.close()

    if platform.system() == "Windows":
        path_open = folder_to_stock_project + "\\" + project_name + "\\" + "root.p4a"
        path_cloud = folder_to_stock_project + "\\" + project_name + "\\" + project_name

    else:
        path_open = folder_to_stock_project + "/" + project_name + "/" + "root.p4a"
        path_cloud = folder_to_stock_project + "/" + project_name + "/" + project_name

    ### reconstruction ###
    project = app.open_project(path_open)
    time1 = datetime.now()
    cluster = project.cluster_at(0)
    cluster.reconstruct().wait()
    time2 = datetime.now()
    reconstruction_time = time2 - time1

    reconstruction = cluster.reconstruction
    if str(reconstruction.status) == "Status.Failed":
        info_file.write("\n------- TIME -------\nadd images time : " + str(add_time)
                        + "\n\n\n")
        info_file.write("ERROR during calibration project : " + project_name + "\n")
        project.save()
        app.quit()
        info_file.close()
        return False

    metrics = reconstruction.metrics

    info_file.write(
        f'Calibrated cameras                          : {(reconstruction.metrics.calibrated_cameras_count)} / {len(cluster.input_cameras)}\n')
    info_file.write(f'points_gsd                                  : {(metrics.points_gsd)}\n ')
    info_file.write(f'median_tracks_count_per_camera              : {(metrics.median_tracks_count_per_camera)}\n ')
    info_file.write(
    f'mean_relative_difference_sensor_parameters  : {(metrics.mean_relative_difference_sensor_parameters)}\n ')

    for index in range(0, metrics.calibrated_cameras_count):
        info_file.write(f'track count for camera  {(index)} : {(metrics.track_count(index))}\n ')

    """for index1 in range(0, metrics.calibrated_cameras_count):
        for index2 in range(0, metrics.calibrated_cameras_count):
            info_file.write(f'track count for camera  pair ({(index1)},{(index2)}) : {(metrics.track_count(index1, index2))} ')
    """
    project.save()
    #project.close()

    ### densify ###
    project = app.open_project(path_open)
    time3 = datetime.now()
    cluster = project.cluster_at(0)
    #cluster.densify().wait()
    densif = cluster.densification
    if str(densif.status) == "Status.Failed":
        info_file.write("\n------- TIME -------\nadd images time : " + str(add_time)
                        + "\ncalibration time : " + str(reconstruction_time)
                        + "\n\n\n")
        info_file.write("ERROR during densification project : " + project_name + "\n")
        project.save()
        app.quit()
        info_file.close()
        return False

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

    reconstruction = cluster.reconstruction
    if str(reconstruction.status) != "Status.Complete":
        info_file.write("ERROR during export clouds : " + project_name + "\n")
        info_file.write("\n------- TIME -------\nadd images time : " + str(add_time)
                        + "\ncalibration time : " + str(reconstruction_time)
                        + "\ndensify time : " + str(densify_time)
                        + "\n\n\n")
        project.save()
        app.quit()
        info_file.close()
        return False

    time7 = datetime.now()
    export_sparse_time = time6 - time5
    export_dense_time = time7 - time6
    project.save()
    project.close()

    info_file.write("\n------- TIME -------\nadd images time : " + str(add_time)
                    + "\ncalibration time : " + str(reconstruction_time)
                    + "\ndensify time : " + str(densify_time)
                    + "\nexport sparse cloud time : " + str(export_sparse_time)
                    + "\nexport dense cloud time : " + str(export_dense_time)
                    + "\n\n\n")

    #app.quit()
    info_file.close()
    return True


test_case(os.environ["Dataset"], os.environ["Folder_to_stock_project"], os.environ["File_info_processing"])




