from pathlib import Path
import os


def split_log(path, split):
    """split the log in several smaller log when it is too big to be read
    Split in megaByte"""
    nbFiles = os.path.getsize(path) // (split*1000000) + 1
    name, extension = os.path.splitext(os.path.basename(path))

    cmd = ""
    for i in range(nbFiles):
        idx = path.index(extension)
        subLog = "'" + path[:idx] + "_" + str(i) + path[idx:]
        cmd = cmd + subLog + "' "
    cmdLine = "split " + path + " -b " + str(split) + "m -d " + cmd
    print(cmdLine)


split_log(r"C:\Users\cwolff\Desktop\FC6310R.log", 1)
