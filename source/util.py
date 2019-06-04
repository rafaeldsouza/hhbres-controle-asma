import requests
import pycep_correios 
import os
import pandas as pd
import numpy as np


def PosicaoGeografica(filtro):
    try:
        retorno = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyAaKE2ndlKTwmX8cVEsc9Ii0EhAiPYwurI"%(filtro))
        res = retorno.json()
        
        if len(res['results'])>0:            
            uf = ""
            result = res['results'][0]
            dados = res['results'][0]['address_components']
            types = ['administrative_area_level_1']
            geonames = filter(lambda x: len(set(x['types']).intersection(types)), dados)
            for geoname in geonames:
                uf = geoname['short_name']
            
            #print(filtro)
            return result['geometry']['location']['lat'],result['geometry']['location']['lng'],uf
        else:
            bairro,cidade,end,uf= EnderecoCep(filtro) 
            if cidade!="":
                filtro = ("%s %s %s %s"%(bairro,cidade,end,uf)).replace('None', '')
                #print(filtro)
                retorno = requests.get("https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=AIzaSyChmZfschQ88vfus-jAG6w1ahl1WC-sLvs"%(filtro))
                res = retorno.json()
                if len(res['results'])>0: 
                    #print(filtro)
                    result = res['results'][0]
                    return result['geometry']['location']['lat'],result['geometry']['location']['lng'],uf
                else:
                    return 0,0,""
            else:
                 return 0,0,""
        
    except:
        print('erro ao consultar o CEP '+str(filtro))
        return 0,0,""
    

def EnderecoCep(cep):
    
    try:
        retorno = pycep_correios.consultar_cep(cep)        
        return retorno["bairro"],retorno["cidade"],retorno["end"],retorno["uf"]
         
    except:
        print('erro ao consultar o CEP '+str(cep))
        return "","","",""

def split(filehandler, delimiter=',', row_limit=1000,
          output_name_template='output_%s.csv', output_path='.', keep_headers=True):
    import csv
    reader = csv.reader(filehandler, delimiter=delimiter)
    current_piece = 1
    current_out_path = os.path.join(
        output_path,
        output_name_template % current_piece
    )
    current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
    current_limit = row_limit
    if keep_headers:
        headers = reader.next()
        current_out_writer.writerow(headers)
    for i, row in enumerate(reader):
        if i + 1 > current_limit:
            current_piece += 1
            current_limit = row_limit * current_piece
            current_out_path = os.path.join(
                output_path,
                output_name_template % current_piece
            )
            current_out_writer = csv.writer(open(current_out_path, 'w'), delimiter=delimiter)
            if keep_headers:
                current_out_writer.writerow(headers)
        current_out_writer.writerow(row)
        
def Buscar(file):
    print("Inicio busca na api")
    dfCEPUnico = pd.read_csv(file)
    for idx, row in dfCEPUnico.iterrows():
    
        lat,long,uf = PosicaoGeografica(str(row["CEP"]).replace(".0","").zfill(8))
        dfCEPUnico.loc[idx,'latitude'] = lat
        dfCEPUnico.loc[idx,'longitude'] = long
        dfCEPUnico.loc[idx,'uf'] = uf
        print("%s:%s %s"%(str(row["CEP"]).replace(".0","").zfill(8),uf,lat))



    dfCEPUnico.to_csv (file, index = None, header=True)
