from flask import Flask, request, redirect
import random
import string
import sqlite3

app = Flask(__name__)
links = {'https://app.powerbi.com/view?r=eyJrIjoiYTY4ZDJmY2QtNjc0Yi00NDcxLWI1YmItNDNmNDVkMmYwNGRjIiwidCI6IjRjZDgzNWY0LTU0NDAtNDA4Zi05M2EzLTk3NWZjMTdjMzg0YSIsImMiOjR9'}

def gerar_codigo(tamanho=6):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choice(caracteres) for _ in range(tamanho))

@app.route('/encurtar', methods=['POST'])
def encurtar():
    url = request.form['url']
    while True:
        codigo = gerar_codigo()
        if codigo not in links:
            break
        links[codigo] = url
    return f"localhost:5000/{codigo}"

@app.route('/<codigo>')
def redirecionar(codigo):
    url = links.get(codigo, None)
    if url:
        return redirect(url)
    return "URL não encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)
