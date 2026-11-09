from flask import Flask, request, render_template, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Configura o banco de dados
def iniciar_banco():
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS links 
                 (codigo TEXT PRIMARY KEY, url_original TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# Gera o código dinâmico baseado na data atual
def gerar_codigo_dinamico():
    agora = datetime.now()  # 03/04/2025
    g = agora.day          # 03
    h = agora.month        # 04
    j = agora.year         # 2025
    k = j * 5              # 10125
    return f"{g:02d}{h:02d}{k}"  # "03410125"

# Salva o link no banco
def salvar_link(url_original):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    codigo = gerar_codigo_dinamico()
    # Verifica se o código já existe e adiciona um sufixo se necessário
    base_codigo = codigo
    sufixo = 1
    while True:
        c.execute("SELECT codigo FROM links WHERE codigo = ?", (codigo,))
        if not c.fetchone():
            break
        codigo = f"{base_codigo}{sufixo:03d}"  # Ex.: 03410125001
        sufixo += 1
    c.execute("INSERT INTO links (codigo, url_original) VALUES (?, ?)", (codigo, url_original))
    conn.commit()
    conn.close()
    return codigo

# Recupera o link do banco
def obter_link(codigo):
    conn = sqlite3.connect('links.db')
    c = conn.cursor()
    c.execute("SELECT url_original FROM links WHERE codigo = ?", (codigo,))
    resultado = c.fetchone()
    conn.close()
    return resultado[0] if resultado else None

# Rota principal com formulário HTML
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url_original = request.form['url']
        codigo = salvar_link(url_original)
        link_curto = f"www.meusite.com/{codigo}"
        return render_template('resultado.html', link_curto=link_curto)
    return render_template('index.html')

# Rota para redirecionamento
@app.route('/<codigo>')
def redirecionar(codigo):
    url = obter_link(codigo)
    if url:
        return redirect(url)
    return "Link não encontrado", 404

if __name__ == "__main__":
    iniciar_banco()
    app.run(debug=True)