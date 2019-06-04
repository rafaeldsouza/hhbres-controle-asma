import pandas as pd
import os
from os import listdir

pastaRaiz = os.path.realpath('..')

def find_csv_filenames( path_to_dir, suffix=".csv" ):
    filenames = listdir(path_to_dir)
    return [ filename for filename in filenames if filename.endswith( suffix ) ]

filenames = find_csv_filenames(pastaRaiz+"/Dados/INMET")
vetPD = []
for name in filenames:
  vetPD.append(pd.read_csv(pastaRaiz+"/Dados/INMET/"+name))
  
df = pd.concat(vetPD)
df.to_csv(pastaRaiz+"/Dados/CLIMA/climaSudeste.csv", index = None, header=True)