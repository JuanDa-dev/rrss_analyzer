
import os
import networkx as nx 
import getopt
import sys
import glob 
import time 

#making a measure of the time execution of the program
start_time = time.time()

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


# Finding x.json.bz2 files in a directory where x is a number 
print(glob.glob("*/*.json.bz2"))
end_time = time.time()
print("Time execution: ", end_time - start_time)




