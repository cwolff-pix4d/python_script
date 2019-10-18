import Pix4Datlas
import os

# To be added to your env
# export IMAGES_PATH = '/home/cpansard/Documents/pix4d/Datasets/data_epfl/'
# export PROJECT_FOLDER = '/home/cpansard/Documents/pix4d/Projects/'

images_path = r"C:\Users\cwolff\Desktop\TESTS\DATA_SETS\data2"
project_folder = r"C:\Users\cwolff\Desktop\TESTS\python-batch"

app = session()
project = app.new_project(project_folder, "Testproject")
project2 = app.open_project(r'C:\Users\cwolff\Desktop\TESTS\190620_exportCloudoyinterpreter_matic550\qa\190620-Negativtest-PyInterpreter\190620-Negativtest-PyInterpreter/root.p4a')
project2.save()
project2.close()
#app.quit()




