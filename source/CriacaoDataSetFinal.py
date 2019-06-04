import pandas as pd
import os
from math import radians, cos, sin, asin, sqrt
import numpy as np
import datetime
pastaRaiz = os.path.realpath('..')

# Formula de Haversine
def haversine( a, b ):
    # Raio da Terra em Km
    r = 6371

    # Converte coordenadas de graus para radianos
    lon1, lat1, lon2, lat2 = map(radians, [ a['longitude'], a['latitude'], b['longitude'], b['latitude'] ] )

    # Formula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    hav = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    d = 2 * r * asin( sqrt(hav) )

    return d


file = pastaRaiz+'/Dados/CEP/CEPCompleto.csv'
dfCEP = pd.read_csv(file)

file = pastaRaiz+'/Dados/clima/estacao_dados.csv'
dfEstacao = pd.read_csv(file)

file = pastaRaiz+'/Dados/SIH-Sudeste/sih2008-2019.csv'
dfSIH = pd.read_csv(file)

file = pastaRaiz+'/Dados/Clima/climaSudeste.csv'
dfClima = pd.read_csv(file)

#adicionar ao dataset as distâncias até a estação de coleta de temperatura mais proximo
dfCEP["codEstacao"]=np.NaN
dfCEP["distancia"]=np.NaN
dfEstacao = dfEstacao[dfEstacao.region == 'Sudeste']
for idx, rowx in dfCEP.iterrows():
    distancia = 99999
    codEstacao = 0
    if rowx["latitude"]!=0.0:
        for idy, rowy in dfEstacao.iterrows():            
            distanciaAux = haversine({'latitude': float(rowx['latitude']), 'longitude': float(rowx['longitude']) },{'latitude': rowy['latitude'], 'longitude': rowy['longitude']})
            if distanciaAux < distancia:
                distancia = distanciaAux
                codEstacao = rowy["codigo_omm"]
        dfCEP.loc[idx,'codEstacao'] = codEstacao
        dfCEP.loc[idx,'distancia'] = distancia

def EstacaoAno(dia, mes):
    if mes in (1, 2):
        return 'VERAO',1
    elif mes == 3:
        if dia < 21:
            return 'VERAO',1
        else:
            return 'OUTONO',2
    elif mes in (4, 5):
        return 'OUTONO',2
    elif mes == 6:
        if dia < 21:
            return 'OUTONO',2
        else:
            return 'INVERNO',3
    elif mes in (7, 8):
        return 'INVERNO',3
    elif mes == 9:
        if dia < 21:
            return 'INVERNO',3
        else:
            return 'PRIMAVERA',4
    elif mes in (10, 11):
        return 'PRIMAVERA',4
    elif mes == 12:
        if dia < 21:
            return 'PRIMAVERA',4
        else:
            return 'VERAO',1


#preparando para fazer o merge de CEP(apenas sudeste) com dados do SIH
dfCEPFiltro = dfCEP[dfCEP.uf.isin(['ES','RJ','SP','MG']) & ((dfCEP.latitude !=0) & (dfCEP.latitude.notnull()))]
dfSIHEstacao = pd.merge(dfSIH,dfCEPFiltro,on='CEP',how='left')

#merge dos dados do SIH com os dados de temperatura coletado por cadas estação
dfClima['DataFormatada'] = pd.to_datetime(dfClima['Data'])
dfSIHEstacao['DT_INTER_Formatado']=pd.to_datetime(dfSIHEstacao.DT_INTER,format='%Y%m%d')
dfSIHFinal = pd.merge(dfSIHEstacao,dfClima[['Estacao','Data','Precipitacao','TempMaxima','TempMinima','Insolacao','Umidade Relativa Media','Velocidade do Vento Media','Unnamed: 11','DataFormatada']],left_on=['codEstacao','DT_INTER_Formatado'],right_on=['Estacao','DataFormatada'],how='left')

#melhorar a qualidade dos dados, removendo os erros referentes a coleta de temperatura
dfSIH = dfSIHFinal[~dfSIHFinal.TempMaxima.isnull()]
dfSIH = dfSIH[dfSIH.TempMaxima!=0]

dfSIH.TempMaxima = pd.to_numeric(dfSIH.TempMaxima)
dfSIH.TempMinima = pd.to_numeric(dfSIH.TempMinima)
dfSIH["TempMedia"] = (dfSIH.TempMaxima+dfSIH.TempMinima)/2

dfSIH["EstacaoAno"]=""
dfSIH["codEstacaoAno"]=0
for idx, row in dfSIH.iterrows():
    data = datetime.datetime.strptime(row['DataFormatada'], '%Y-%m-%d')
    estacao,codEstacao = EstacaoAno(data.day,data.month)
    dfSIH.loc[idx,"EstacaoAno"]=estacao
    dfSIH.loc[idx,"codEstacaoAno"]=codEstacao

dfSIH["FaixaEtaria"]=""
dfSIH["CodFaixaEtaria"]=0

dfSIH.loc[dfSIH['IDADE'] <= 5, ['FaixaEtaria','CodFaixaEtaria']] = "0-5",1
dfSIH.loc[(dfSIH['IDADE'] > 5) & (dfSIH['IDADE'] <= 12), ['FaixaEtaria','CodFaixaEtaria']] = "6-12",2
dfSIH.loc[(dfSIH['IDADE'] > 12) & (dfSIH['IDADE'] <= 19), ['FaixaEtaria','CodFaixaEtaria']] = "13-19",3
dfSIH.loc[(dfSIH['IDADE'] > 19) & (dfSIH['IDADE'] <= 55), ['FaixaEtaria','CodFaixaEtaria']] = "20-55",4
dfSIH.loc[(dfSIH['IDADE'] > 55), ['FaixaEtaria','CodFaixaEtaria']] = "55 ou mais",5

dfSIH.to_csv (pastaRaiz+"/Dados/Final/SIHFinal.csv", index = None, header=True)

