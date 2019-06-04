from pandas.compat import StringIO
import pandas as pd 
import requests
import bs4
import os

pastaRaiz = os.path.realpath('..')
file = pastaRaiz+'/Dados/CLIMA/estacao_dados.csv'
df = pd.read_csv(file)

df_sudeste = df[df.region == 'Sudeste']

session = requests.Session()

data = {}
data['mCod'] = input("Informe o e-mail cadastrado no INMET: ")
data['mSenha'] = input("Informe a senha: ")
#"mi2urrmw"
response = session.post('http://www.inmet.gov.br/projetos/rede/pesquisa/inicio.php', data)

len(df_sudeste)
data_inicio = input("Informe a data inicial (dd/MM/yyyy): ")#"01/01/2008"
data_fim = input("Informe a data final (dd/MM/yyyy): ")#"04/03/2019"
    
for index, row in df_sudeste.iterrows():
    
    OMM = str( row['codigo_omm'])
    #Estacao;Data;Hora;Temp Comp Media;Umidade Relativa Media;Velocidade do Vento Media;

    url = "http://www.inmet.gov.br/projetos/rede/pesquisa/gera_serie_txt.php?"
    atributos = "&mAtributos=,,1,1,,,,,,1,1,,1,1,1,1,"
    url_param = "&mRelEstacao="+OMM+"&btnProcesso=serie&mRelDtInicio="+data_inicio+"&mRelDtFim="+data_fim+atributos
    url = url + url_param
    
    response = session.get(url)
    text = response.content
    soup = bs4.BeautifulSoup(text, 'html.parser')
    table_body = soup.find("pre")
    arquivo = pastaRaiz+"/Dados/INMET/%s_%s_%s.csv"%(row["state"],row["station_name"],row["codigo_omm"])
        
    if(table_body is not None):
        dfTempo = pd.read_csv(StringIO(table_body.contents[2].split("--------------------")[1]),';')
        dfTempo = dfTempo.groupby(['Estacao','Data']).sum().reset_index()

        dfTempo["station_name"]=row["station_name"]
        dfTempo["state"]=row["state"]
        dfTempo["state_initials"]=row["state_initials"]
        dfTempo["region"]=row["region"]
        dfTempo["latitude"]=row["latitude"]
        dfTempo["longitude"]=row["longitude"]
        dfTempo["altitude"]=row["altitude"]
        dfTempo.to_csv (arquivo, index = None, header=True) 
        print(arquivo)
    else:
        print("Erro no ao gerar o arquivo "+arquivo)
