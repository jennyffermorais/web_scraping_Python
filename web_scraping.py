import requests
from bs4 import BeautifulSoup
import json
import os

# Pegando o conteúdo HTML a partir da URL
url = 'https://gizmodo.uol.com.br'

req = requests.get(url)

soup = BeautifulSoup(req.content, 'html.parser')

lista_noticias = soup.find_all('div', class_='block--split clearfix')

titulos = []
resumos = []
datas = []

# Pegando os dados do site
for lista_posts in lista_noticias:
    pegar_titulo = lista_posts.find_all('h3', class_='postTitle entry-title')
    pegar_data = lista_posts.find_all('span', class_='metaText metaDate')
    pegar_resumo = lista_posts.find_all('div', class_='postSummary entry-content')
    num_posts = 10

    for i in range(num_posts):
        titulo = pegar_titulo[i].a.next_element
        titulos.append(titulo)
        data = pegar_data[i].abbr.next_element
        datas.append(data)
        resumo = pegar_resumo[i].p.next_element
        resumos.append(resumo)

# Criando o dicionário
dicionario = {
    "titulo": titulos,
    "data": datas,
    "resumo": resumos
}

# Convertendo o dicionário para um json
json_dicio = json.dumps(dicionario)

# Deleta o arquivo json caso ele já exista
if os.path.exists("meu_dicionario.json"):
    os.remove("meu_dicionario.json")

# Cria e escreve no arquivo json
arquivo = open("meu_dicionario.json", "a")
arquivo.write(json_dicio)
arquivo.close()

# Deleta o arquivo csv caso ele já exista
if os.path.exists("meu_dicionario.CSV"):
    os.remove("meu_dicionario.CSV")

# Cria as linhas do arquivo csv
CSV = ""
for i in range(10):
    line = "{}\t{}\t{}\n".format(dicionario['titulo'][i], dicionario['data'][i], dicionario['resumo'][i])
    CSV += line

# Cria e escreve no arquivo csv
arquivo = open("meu_dicionario.CSV", "a")
arquivo.write(CSV)
arquivo.close()