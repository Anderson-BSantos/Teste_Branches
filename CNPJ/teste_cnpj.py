#pip install pandas requests schedule time BeautifulSoup4 StingsIO
import matplotlib.pyplot as plt
import pandas as pd
import requests
import schedule
import time
from bs4 import BeautifulSoup
from io import StringIO  # Importar diretamente StringIO


def fetch_data():
    url = 'https://sidra.ibge.gov.br/geratabela/DownloadSelecaoComplexa/-1131028881'
    response = requests.get(url)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        try:
            print("Conteúdo da resposta (primeiros 500 caracteres):")
            print(response.text[:500])  # Verifique o conteúdo da resposta

            data = response.content.decode('utf-8')  # Decodificar o conteúdo
            df = pd.read_csv(StringIO(data))  # Ler o CSV
            print(f"DataFrame carregado. Dimensões: {df.shape}")
            print(df.head())  # Exibir as primeiras linhas do DataFrame

        except Exception as e:
            print(f"Erro ao processar os dados: {e}")
    else:
        print('Falha ao buscar os dados')

# Chamar a função para testar
fetch_data()

# O código abaixo trata-se de um agendamento para execução da função fetch_data
'''
# Schedule the fetch_data function to run every day at 10 AM
schedule.every().day.at("07:00").do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)
'''       

