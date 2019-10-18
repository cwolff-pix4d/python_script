import xml.etree.ElementTree as ET
from pathlib import Path
from datetime import datetime


def p4d2gcps_file(pix4d_file):

    xmlp4d = ET.parse(pix4d_file)
    root = xmlp4d.getroot()

    gcp_path = str(Path(pix4d_file).parent.absolute()) + "/gcps.txt"
    gcp_file = open(gcp_path, "w")

    for gcp in root.iter('GCP'):
        # creation of each GCP with info given by xml file
        gcp_file.write(str(gcp.get('id')) +  "," + str(gcp.get('x')) + "," + gcp.get('y') + "," + gcp.get('z') + "\n")
    gcp_file.close()
    return 0

def timeLapse_calib(t1,t2):
    datetime1 = datetime.strptime(t1, '%Y.%m.%d %H:%M:%S')
    datetime2 = datetime.strptime(t2, '%Y.%m.%d %H:%M:%S')
    delta = datetime2 - datetime1
    return(str(delta))

def timeLapse_matic(t1,t2):
    datetime1 = datetime.strptime(t1, '%Y-%m-%d %H:%M:%S')
    datetime2 = datetime.strptime(t2, '%Y-%m-%d %H:%M:%S')
    delta = datetime2 - datetime1
    return(str(delta))

def timeCalib_maticVScalib(logCalib, logMatic):
    fileCalib = open(logCalib, "r")
    fileMatic = open(logMatic, "r")
    linesCalib = fileCalib.readlines()
    linesMatic = fileMatic.readlines()
    fileCalib.close()
    fileMatic.close()

    for line in linesCalib:
        if "************ Keypoints       ************************" in line:
            KeypointsC = line[1:20]
        if "************ matching        ************************" in line:
            MatchingC = line[1:20]
        if "*********CalibrateSeq**********" in line:
            CalibrateSeqC = line[1:20]
        if "****Cluster done*******" in line:
            ClusterC = line[1:20]
        if "*******GeoreferenceProcessing**" in line:
            GeoreferenceProcessingC = line[1:20]
        if "******* GCPProcessing *********" in line:
            GCPProcessingC = line[1:20]
        if "*******InitialReportCalib********" in line:
            InitialReportCalibC = line[1:20]
    print("*****  TIME IN CALIB APP *****"
          " -- Processing time : ", timeLapse_calib(KeypointsC,InitialReportCalibC),\
          "\n\n -- Keypoints : ", timeLapse_calib(KeypointsC,MatchingC),\
    "\n -- Matching : ", timeLapse_calib(MatchingC,CalibrateSeqC),\
    "\n -- CalibrateSeq : ", timeLapse_calib(CalibrateSeqC,ClusterC),\
    "\n -- Cluster : ", timeLapse_calib(ClusterC,GeoreferenceProcessingC),\
    "\n -- GeoreferenceProcessing : ", timeLapse_calib(GeoreferenceProcessingC,GCPProcessingC),\
    "\n -- GCPProcessing : ", timeLapse_calib(GCPProcessingC,InitialReportCalibC))

    InitialReportCalibM = None
    for line in linesMatic:
        if "************ Keypoints       ************************" in line:
            KeypointsM = line[0:19]
        if "************ matching        ************************" in line:
            MatchingM = line[0:19]
        if "*********CalibrateSeq**********" in line:
            CalibrateSeqM = line[0:19]
        if "****Cluster done*******" in line:
            ClusterM = line[0:19]
        if "*******GeoreferenceProcessing**" in line:
            GeoreferenceProcessingM = line[0:19]
        if "******* GCPProcessing *********" in line:
            GCPProcessingM = line[0:19]
        if "[Calibrate cameras] Finished" in line:
            InitialReportCalibM = line[0:19]
        if InitialReportCalibM == None:
            InitialReportCalibM = linesMatic[len(linesMatic) - 1][0:19]
    print("\n\n*****  TIME IN MATIC *****"
          " -- PROCESSING TIME : ", timeLapse_matic(KeypointsM,InitialReportCalibM),\
          "\n\n -- Keypoints : ", timeLapse_matic(KeypointsM,MatchingM),\
    "\n -- Matching : ", timeLapse_matic(MatchingM,CalibrateSeqM),\
    "\n -- CalibrateSeq : ", timeLapse_matic(CalibrateSeqM,ClusterM),\
    "\n -- Cluster : ", timeLapse_matic(ClusterM,GeoreferenceProcessingM),\
    "\n -- GeoreferenceProcessing : ", timeLapse_matic(GeoreferenceProcessingM,GCPProcessingM),\
    "\n -- GCPProcessing : ", timeLapse_matic(GCPProcessingM,InitialReportCalibM))
    return 0



def sec2min2hour(sec):
    hour = sec // 3600
    sec = sec % 3600
    min = sec // 60
    sec = sec % 60
    print(hour, ":", min, ":", sec)
    return hour, min, sec


def timeCalibDense(sec_C, sec_D):
    print("calib :")
    sec2min2hour(sec_C)
    print("dense :")
    sec2min2hour(sec_D)
    print("calib and dense :")
    sec2min2hour(sec_C + sec_D)

#timeCalib_maticVScalib(r"C:\Users\cwolff\Downloads\TESTS\logs_calib\C080_calib.log", r"C:\Users\cwolff\Downloads\TESTS\logs_matic\C080_matic_log.txt")
#p4d2gcps_file()


timeCalibDense(123640,118295)
#sec2min2hour(121579)