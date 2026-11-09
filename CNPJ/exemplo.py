import requests
import pandas as pd
import schedule
import time
from bs4 import BeautifulSoup

def fetch_data():
    url = 'https://sidra.ibge.gov.br/geratabela/DownloadSelecaoComplexa/398980661'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
        df = pd.read_csv(pd.compat.StringIO(data.decode('utf-8')))
        # Process the data as needed
        print(df.head())
    else:
        print('Failed to fetch data')

# Schedule the fetch_data function to run every day at 10 AM
schedule.every().day.at("10:00").do(fetch_data)

while True:
    schedule.run_pending()
    time.sleep(1)