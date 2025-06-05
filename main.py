from flask import Flask, request, jsonify, redirect
from baixar_imagem import buscar_imagem, sanitize_filename
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Rota que retorna JSON com a URL da imagem (útil para testes via navegador ou API)
@app.route("/buscar_imagem")
def buscar():
    marca = request.args.get("marca", "")
    modelo = request.args.get("modelo", "")
    cor = request.args.get("cor", "")
    ano = request.args.get("ano", "")
    
    url = buscar_imagem(marca, modelo, cor, ano)
    if url:
        return jsonify({"url": url})
    else:
        return jsonify({"erro": "Imagem não encontrada"}), 404

# Rota que redireciona diretamente para a imagem (para uso direto no <img src=...>)
@app.route("/imagens/<path:nome_arquivo>")
def imagens(nome_arquivo):
    # Remove extensão e extrai partes do nome
    nome = nome_arquivo.replace(".jpg", "")
    partes = nome.split("_")
    
    if len(partes) < 4:
        return jsonify({"erro": "Formato inválido"}), 400
    
    marca = partes[0]
    modelo = "_".join(partes[1:-2])
    cor = partes[-2]
    ano = partes[-1]

    url = buscar_imagem(marca, modelo, cor, ano)
    if url:
        return redirect(url)
    else:
        return jsonify({"erro": "Imagem não encontrada"}), 404

# Rota de teste opcional
@app.route("/")
def index():
    return "API de busca de imagens de veículos - OK"

if __name__ == "__main__":
    app.run(debug=True)
