import pandas as pd
import numpy as np
import util
import os
pastaRaiz = os.path.realpath('..')

file = pastaRaiz+'/Dados/SIH-Sudeste/sih2008-2019.csv'
dfSIH = pd.read_csv(file)


dfCEPUnico = pd.DataFrame({'CEP':dfSIH["CEP"].unique()})

print(len(dfSIH["CEP"].unique()))

dfCEPUnico["longitude"]=np.nan
dfCEPUnico["latitude"]=np.nan
dfCEPUnico["uf"]=np.nan

print("Inicio busca na api")

#dfCEPUnico[['latitude','longitude','uf']] = dfCEPUnico['CEP'].apply(lambda x: pd.Series(util.PosicaoGeografica(str(x))))

for idx, row in dfCEPUnico.iterrows():
    
    lat,long,uf = util.PosicaoGeografica(str(row["CEP"]).replace(".0",""))
    dfCEPUnico.loc[idx,'latitude'] = lat
    dfCEPUnico.loc[idx,'longitude'] = long
    dfCEPUnico.loc[idx,'uf'] = uf



dfCEPUnico.to_csv (pastaRaiz+"/Dados/CEP/CEPCompleto.csv", index = None, header=True)

print("FIM")