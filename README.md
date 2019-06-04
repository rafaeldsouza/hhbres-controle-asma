# Desafio No Controle da Asma
No Controle da Asma, o 1° Datathon em Saúde da GSK Brazil acontecerá de 17 de maio a 02 de junho de 2019, com duração de 15 dias para gerar novos insights sobre a asma no Brasil a partir de dados abertos e formas inovadoras de visualização.

# Sobre o desafio
Gerar dados sobre o real impacto da asma na saúde pública do Brasil, uma vez que faltam dados sobre o cenário da asma do país na perspectiva de diagnóstico, internação, custos, mortalidade, fatores estruturais, sociais e ambientais.

# Abordagem

Para esse desafio fizemos um extraimos os casos de asma (CID-J45) da base de dados [SIH](http://www2.datasus.gov.br/DATASUS/index.php?area=0901&item=1&acao=25) com o clima obtido da base [INMET](http://www.inmet.gov.br/portal/index.php?r=bdmep/bdmep), com o intuito de fazer um paraledo dos casos de asma com as mudanças climaticas.

# Tratamento dos dados

Um dos grandes desafios que tivemos foi o tratamento dos dados. Iniciamos fazendo o filtro dos dados baixados do DATASUS utilizando o TabWin que está disponivel junto com os dataset. Após selecionar os dados da região sudeste e filtrar pelo CID J45 exportamos em o arquivo CVS Dados/SIH-Sudeste/sih2008-2019.cvs.

Analisando os dados do SIH, percebemos que a unica forma de juntar os dados com a base de clima seria transformando o CEP do paciente em Latitude e Longitude, e para isso usamos a [API Geocoding do Google](https://developers.google.com/maps/documentation/geocoding/start). 

Ao fazer a busca no Geocoding por meio dos CEPs,  alguns deles não foram encontrados. Devido a isso, para trazer mais confiança aos dados, foi utilizado uma api que usa a base dos Correios (PyCep-correios) por meio do endereço completo. Dessa forma, buscamos novamente os dados no Geocoding.  Foram descartados CEPs que estavam invalidos ou que eram de outras regiões diferentes, no total 15057 CEPs foram descartados de um total de 75464 CEPs distintos dos pacientes.

Após obter a Latitude e Longitude baseado nos CEP dos pacientes, utilizando o Geocoding, foi feito o cruzamento dos dados com a base de clima, e para isso, foi feito utilizado o algoritimo de **Haversine** e utilizado a estação de coleta de Clima mais proximo.

# Visualização dos dados

A visualização dos dados foi feita no PowerBI(hhbres-asma.pbix), onde foram criados as seguintes visões:
* Caso de Asma por temperatura média.
* Casos de Asma separando por Faixa Etária e Estação do Ano.
* Relação de custo por Faixa Etária, por Estação do Ano e por Mês.
* Relação de custo médio por Faixa Etária, por Estação do Ano e por Mês.
* Distribuição dos casos na região sudeste.

## Apresentação dos dados
[Painel publicado](https://app.powerbi.com/view?r=eyJrIjoiNDY3ODJkNzctNWIwNi00ZDZjLThkMjgtYWRiOWZmMWJiYmY3IiwidCI6ImNiOTk1MDM4LWIxZGYtNGViYy04YTc4LTg4YjViYjUxNmE1YiIsImMiOjl9)
### Casos de asma por temperatura média
![alt text](https://github.com/rafaeldsouza/hhbres-controle-asma/blob/master/imagens/casos%20por%20temperatura.jpg "Casos de asma por temperatura média")

### Casos de Asma separando por Faixa Etária e Estação do Ano
![alt text](https://github.com/rafaeldsouza/hhbres-controle-asma/blob/master/imagens/por%20idade.jpg "Casos de Asma separando por Faixa Etária e Estação do Ano")

### Relação de custo por Faixa Etária, por Estação do Ano e por Mês.
![alt text](https://github.com/rafaeldsouza/hhbres-controle-asma/blob/master/imagens/custo%20total.jpg "Relação de custo por Faixa Etária, por Estação do Ano e por Mês.")

### Relação de custo médio por Faixa Etária, por Estação do Ano e por Mês.
![alt text](https://github.com/rafaeldsouza/hhbres-controle-asma/blob/master/imagens/custo%20medio.jpg "Relação de custo médio por Faixa Etária, por Estação do Ano e por Mês.")

### Distribuição dos casos na região sudeste.
![alt text](https://github.com/rafaeldsouza/hhbres-controle-asma/blob/master/imagens/mapa.png "Distribuição dos casos na região sudeste.")


# Potencial do Código

Enxergamos um potencial preditivo eficaz com o código apresentado, devido a mineração e tratamento dos dados ter sido feita de forma parcimoniosa e supervisionada, com o cruzamento de dados, em especial da temperatura, meses, e número de casos, que corroboram com o esperado das literaturas.

Devido a isso, esse código tem potencial preditivo no que tange a estimar quantos casos ocorrerão em um dado mês, com determinada temperatura. Além disso, com os dados de custo, enxergamos potencial em ele estimar o quanto será gasto com a asma em certa estação ou período do ano e futuras atualizações, acreditamos que ele consiga estimar o quão benéfica será determinada intervenção para o problema da asma, tanto em relação a redução de casos, quanto na diminuição dos custos.

# Equipe HHBRES - Controle Asma
[Matheus Silva Santos](https://github.com/matheusses)

[Rafael de Souza Conceição](https://github.com/rafaeldsouza)

[Willer Fiorotti](https://github.com/WillerFiorott)
