#import Pix4Dmatic
import os
import shutil
from datetime import datetime
import platform
import sys
import numpy as np
import pandas as pd


from pix4dengine import create_project, process_project, open_project
from pix4dengine.enginewrapper import EngineWrapper
from pix4dengine.constants.processing import ProcessingStep

###### TO COMPLETE
os.environ["template"] = r"\\devsynology\Perftracker\Projects\pix4dmaticBenchmark\QAresult_maticVSmapper\compare_maticVSmapper.tmpl"
os.environ["mapper"] = "C:\Program Files\Pix4Dmapper\pix4dmapper.exe"
mail_adress = "charlotte.wolff@pix4d.com"
password = "Cpm9chL8.32"
######

class Camera:
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.x_matic = []
        self.y_matic = []
        self.z_matic = []
        self.x_mapper = []
        self.y_mapper = []
        self.z_mapper = []
        self.matic_mean = 0
        self.mapper_mean = 0

    def mean_matic(self):
        print(self.x_matic)
        print(self.matic_mean)
        x_mean = np.mean(np.asarray(self.x_matic))
        y_mean = np.mean(np.asarray(self.y_matic))
        z_mean = np.mean(np.asarray(self.z_matic))
        self.matic_mean = [x_mean, y_mean, z_mean]

    def mean_mapper(self):
        x_mean = np.mean(np.asarray(self.x_mapper))
        y_mean = np.mean(np.asarray(self.y_mapper))
        z_mean = np.mean(np.asarray(self.z_mapper))
        self.mapper_mean = [x_mean, y_mean, z_mean]

    def MEAN(self):
        self.mean_mapper()
        self.mean_matic()

def txt_to_df(txt_path):
    df = pd.read_table(txt_path, delim_whitespace=True, index_col=0)
    return df

def create_cameras(images_paths):
    list_cameras = []
    for img in os.listdir(images_paths):
        new_camera = Camera(img, os.path.join(images_paths, img).replace("\\", "/"))
        list_cameras.append(new_camera)
    return list_cameras


def test_case_MATIC(list_cameras, dataset, folder_to_stock_project, file_info_processing, n):
    process = dataset.split(";")[0]
    project_name = dataset.split(";")[1]
    images_path = dataset.split(";")[2]
    gcps_path = dataset.split(";")[3]
    comment = dataset.split(";")[4]
    file_info_processing = file_info_processing + "_matic_" + project_name + ".txt"

    info_file = open(file_info_processing, "a")
    info_file_name, info_file_extension = os.path.splitext(os.path.basename(file_info_processing))
    info_file.write("Results for processing : " + info_file_name + "\n" + str(datetime.now()) + "\n\n\n")
    info_file.write("************************\n")
    info_file.write(project_name + "\n")
    info_file.write("note :        {(comment)}\n")

    ### add gcps and imgs ###
    app = session()
    project = app.new_project(folder_to_stock_project, project_name)
    cluster = project.cluster_at(0)
    cluster.add_images_from(images_path).wait()
    images = cluster.input_cameras
    #project.info("SHIFT CAMERA :      " + str(cluster.ref_frame.shift) + "\n")

    if str(images.status) == "Status.Failed":
        info_file.write("Error during the import of images : " + project_name + "\n")
        app.quit()
        info_file.close()
        return False
    if platform.system() == "Windows":
        path_open = folder_to_stock_project + "\\" + project_name + "\\" + "root.p4a"
        path_cloud = folder_to_stock_project + "\\" + project_name + "\\" + project_name

    else:
        path_open = folder_to_stock_project + "/" + project_name + "/" + "root.p4a"
        path_cloud = folder_to_stock_project + "/" + project_name + "/" + project_name

    ### reconstruction ###
    for i in range(n):
        cluster.reconstruct().wait()
        reconstruction = cluster.reconstruction
        if str(reconstruction.status) == "Status.Failed":
            info_file.write("ERROR during calibration project : " + project_name + "\n")
            app.quit()
            info_file.close()
            return False
        reconstruction = cluster.reconstruction
        calibCameras = reconstruction.calibrated_cameras
        pos_calibCameras = calibCameras.positions
        session().project_at(0).info(str(pos_calibCameras))
        for i_calib in range(len(calibCameras)):
            for j_input in range(len(list_cameras)):
                if calibCameras.paths[i_calib] == list_cameras[j_input].path:
                    list_cameras[j_input].x_matic.append(pos_calibCameras[i_calib][0])
                    list_cameras[j_input].y_matic.append(pos_calibCameras[i_calib][1])
                    list_cameras[j_input].z_matic.append(pos_calibCameras[i_calib][2])
    for i in range(len(list_cameras)):
        list_cameras[i].mean_matic()
        info_file.write(list_cameras[i].name + " mean (x - y - z): " + str(list_cameras[i].matic_mean) + "\n")
    info_file.close()
    app.quit()
    return list_cameras


def test_case_MAPPER(list_cameras, dataset, folder_to_stock_project, file_info_processing, n=5):
    process = dataset.split(";")[0]
    project_name = dataset.split(";")[1]
    images_path = dataset.split(";")[2]
    gcps_path = dataset.split(";")[3]
    comment = dataset.split(";")[4]

    file_info_processing = str(file_info_processing) + "_mapper_" + project_name + ".txt"

    info_file = open(file_info_processing, "a")
    info_file_name, info_file_extension = os.path.splitext(os.path.basename(file_info_processing))
    info_file.write("Results for processing : " + info_file_name + "\n" + str(datetime.now()) + "\n\n\n")
    info_file.write("************************\n")
    info_file.write(project_name + "\n")


    if process != "*":
        engine_wrapper = EngineWrapper(base_command=os.environ["mapper"], max_cpus=10)
        if engine_wrapper.is_logged_in():
            engine_wrapper.logout()
        if not engine_wrapper.is_logged_in():
            engine_wrapper.login(mail_adress, password)

        # add images
        work_dir = (os.path.join(folder_to_stock_project, project_name))
        i = 0
        work_dir = str(work_dir) + str(i)
        while os.path.isdir(work_dir):
            i+=1
            work_dir = str(work_dir) + str(i)
        project = create_project(project_name, images_path, engine_wrapper,
                                 template=os.environ["template"],
                                 work_dir=work_dir)
        calib_file_path = str(os.path.join(work_dir, project_name) + "\\1_initial\\params\\" + project_name + "_calibrated_external_camera_parameters.txt")
        for i in range(n):
            # calibration
            process_project(project, engine_wrapper, steps=ProcessingStep.CALIB)
            calib_file = txt_to_df(calib_file_path)
            camera_name = list(calib_file.index.values)
            #camera_name = calib_file.index()[0]
            for i_input in range(len(list_cameras)):
                for j_calib in range(len(camera_name)):
                    if str(camera_name[j_calib]) == str(list_cameras[i_input].name):
                        list_cameras[i_input].x_mapper.append(calib_file.loc[str(camera_name[j_calib]), 'X'])
                        list_cameras[i_input].y_mapper.append(calib_file.loc[str(camera_name[j_calib]), 'Y'])
                        list_cameras[i_input].z_mapper.append(calib_file.loc[str(camera_name[j_calib]), 'Z'])
    print(list_cameras[0].x_mapper)
    for i in range(len(list_cameras)):
        list_cameras[i].mean_mapper()
        info_file.write(list_cameras[i].name + " mean (x - y - z): " + str(list_cameras[i].mapper_mean) + "\n")
    info_file.close()
    return list_cameras

images_path = os.environ["Dataset"].split(";")[2]
list_cameras = create_cameras(images_path)
#list_cameras = test_case_MAPPER(list_cameras, os.environ["Dataset"], os.environ["Folder_to_stock_project"],0,2)
list_cameras = test_case_MATIC(list_cameras, os.environ["Dataset"], os.environ["Folder_to_stock_project"], os.environ["File_info_processing"],10)

