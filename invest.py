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
    return response.json()

# Lista de ações que você deseja monitorar
acoes = {
    'SYNE3.SA': 4.80,   # Ação da SYN - Alvo de preço de R$4,80
    # 'PETR4.SA': 32,   # Ação da Petrobras - Alvo de preço de R$38
    # 'BBAS3.SA': 25,   # Ação da Banco do Brasil - Alvo de preço de R$25
    # 'BBDC3.SA': 10.40,   # Ação da Bradesco - Alvo de preço de R$10,40
    # 'TAEE4.SA': 10.90,   # Ação da Taesa - Alvo de preço de R$10,90
    # 'JHSF3.SA': 3.60,   # Ação da JHSF - Alvo de preço de R$3,60
    # 'IAAG11.SA': 7.35,  # Ação da IAAG11 - Alvo de preço de R$7.35
    # 'BTCI11.SA': 7.75,  # Ação da  - Alvo de preço de R$7.75
}

# Dicionário para armazenar o último preço notificado
ultimos_precos = {}

# Função principal para verificar o preço
def verificar_precos():
    while True:
        for acao, preco_alvo in acoes.items():
            # Obtém a cotação atual da ação
            ticker = yf.Ticker(acao)
            preco_atual = ticker.history(period='1d')['Close'].iloc[0]
            print(f"{acao}: {preco_atual} - Alvo: {preco_alvo}")
            
            # Verifica se o preço alvo é menor que o preço atual e ainda não foi notificado
            if (preco_atual - preco_alvo) <= 0:
                if acao not in ultimos_precos or ultimos_precos[acao] > preco_alvo:
                    texto = f"O preço da ação {acao} caiu para R${preco_atual:.2f}. Alvo de R${preco_alvo:.2f} atingido!"
                    enviar_telegram_mensagem(texto)
                    print(f"Notificação enviada para {acao}!")

                    # Atualiza o último preço notificado
                    ultimos_precos[acao] = preco_alvo
        
        # Intervalo de 60 segundos para verificar novamente
        print("------------------------------------------------")
        time.sleep(60)

# Chama a função para começar a monitorar 
verificar_precos()
