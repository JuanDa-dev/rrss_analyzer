
import os
import networkx as nx 
import glob 
import json 
import shutil,bz2,getopt,sys
from collections import defaultdict
import bz2 

# Get command line arguments
fecha_inicial = None
fecha_final = None
hashtag = None

try:
    opts, args = getopt.getopt(sys.argv[1:], "d:fi:ff:h:grt:jrt:gm:jm:gcrt:jcrt")

    for o,a in opts:
        if o == "-d":
            print("Directorio: ", a)
        elif o == "-fi":
            print("Fecha inicial: ", a)
        elif o == "-ff":
            print("Fecha final: ", a)
        elif o == "-h":
            print("Nombre de archivo ", a) #Hastag
        elif o == "-grt":
            print("Grafo de retweets: ", a)
        elif o == "-jrt":
            print("JSON de retweets: ", a)
        elif o == "-gm":
            print("Grafo de menciones: ", a)
        elif o == "-jm":
            print("JSON de menciones: ", a)
        elif o == "-gcrt":
            print("Grafo de componentes retweets: ", a)
        elif o == "-jcrt":
            print("JSON de componentes retweets: ", a)
        else:
            assert False, "unhandled option"

except getopt.GetoptError as err:
    # print help information and exit:
    print(err)  # will print something like "option -a not recognized"
    sys.exit(2)

# Looking for json.bz2 files in the directory
file_list = glob.glob("*/*.json.bz2")

# Decompressing in json file 
for file_path in file_list:
    with bz2.open(file_path, "rb") as input_file:
        # Read the compressed data
        compressed_data = input_file.read()
        
        # Get the output file name by removing the ".bz2" extension
        output_file_name = os.path.splitext(file_path)[0]
        
        # Write the decompressed data to the output file
        with open(output_file_name, "w") as output_file:
            output_file.write(compressed_data.decode("utf-8"))





# #Filtter by fi and ff 
# if opts[1] == "-fi":
#     file_list = [x for x in file_list if x.split("/")[0] >= opts[2]]
# if opts[3] == "-ff":
#     file_list = [x for x in file_list if x.split("/")[0] <= opts[4]]
# else:
#     pass









