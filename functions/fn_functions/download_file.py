import zipfile
import requests
from io import BytesIO
import os

BASE_PATH = '/opt/ml/processing/output'
CENSO_PATH = f"{BASE_PATH}/censo"

if __name__ == "__main__" :
    #   CRIANDO UM DIRETORIO PARA ARMAZENAR O CONTÚDO DO CENSO
    os.makedirs(CENSO_PATH, exist_ok=True)

    #   DEFINE ARGS PARA O DOWNLOAD
    url = 'https://download.inep.gov.br/dados_abertos/microdados_censo_escolar_2020.zip'
    filebytes = BytesIO(requests.get(url, stream=True).content)

    #   EXTRAINDO OS DADOS
    myzip = zipfile.ZipFile(filebytes)
    myzip.extractall(CENSO_PATH)