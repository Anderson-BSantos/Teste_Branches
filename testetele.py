import yfinance as yf
import time
import requests

# Token do seu Bot do Telegram
BOT_TOKEN = '7718257093:AAEdIvLYltooDONigsSt3obhaJ7ZXjQxAok'
# O ID do seu chat ou grupo do Telegram
CHAT_ID = '1162695392'

# Função para enviar mensagem via Telegram
def enviar_telegram_mensagem(texto):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    params = {
        'chat_id': CHAT_ID,
        'text': texto
    }
    response = requests.get(url, params=params)
    response_json = response.json()
    
    # Verifica se a resposta foi bem-sucedida
    if response_json.get("ok"):
        print(f"Notificação enviada com sucesso: {texto}")
    else:
        print(f"Erro ao enviar notificação: {response_json}")
    
    return response_json

# Lista de ações que você deseja monitorar
acoes = {
    'AAPL': 150,  # Ação da Apple - Alvo de preço de R$150
    'GOOGL': 2700,  # Ação do Google - Alvo de preço de R$2700
    'AMZN': 3300  # Ação da Amazon - Alvo de preço de R$3300
}

# Função principal para verificar o preço
def verificar_precos():
    while True:
        for acao, preco_desejado in acoes.items():
            # Obtém a cotação atual da ação
            ticker = yf.Ticker(acao)
            preco_atual = ticker.history(period='1d')['Close'].iloc[0]
            print(f"{acao}: {preco_atual} - Alvo: {preco_desejado}")
            
            # Verifica se o preço atingiu o valor desejado
            if preco_atual >= preco_desejado:
                texto = f"O preço da ação {acao} atingiu R${preco_atual}. Alvo de R${preco_desejado} alcançado!"
                print("Preço alvo atingido! Enviando notificação...")
                response = enviar_telegram_mensagem(texto)
                print(f"Resposta da API do Telegram: {response}")
        
        # Intervalo de 60 segundos para verificar novamente
        time.sleep(60)

# Chama a função para começar a monitorar
verificar_precos()
