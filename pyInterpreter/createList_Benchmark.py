import os, fnmatch


def create_Benchmark(path_Benchmark, fileName):

    file = open(os.path.join(path_Benchmark,fileName), 'w')
    nb = 0
    for root, dirs, files in os.walk(path_Benchmark):
        if len(dirs) > 0:
            del dirs[0]
        for name in dirs:
            path = os.path.join(root, name)
            pattern = "*.txt"
            listOfFiles = os.listdir(path)

            gcp = "N"
            for entry in listOfFiles:
                if fnmatch.fnmatch(entry, pattern):
                    if entry[0:4] == "gcps":
                        gcp = entry

            nb += 1
            line = str(str(nb) + ";" + name + ";" + os.path.join(root, name) + ";" + gcp + "\n")
            file.write(line)
    file.close()



# MAIN
path_Benchmark = r"\\devsynology\Perftracker\Projects\pix4dmaticBenchmark\small_cs"
fileName = "cs_List_WIN.txt"
create_Benchmark(path_Benchmark, fileName)


path_Benchmark = r"\\devsynology\Perftracker\Projects\pix4dmaticBenchmark\small_cameras"
fileName = "cameras_List_WIN.txt"
create_Benchmark(path_Benchmark, fileName)
