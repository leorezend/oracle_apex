from flask import Flask, send_file, abort
from baixar_imagem import baixar_e_retornar_caminho, montar_termos
import os

app = Flask(__name__)

@app.route('/imagens/<path:arquivo>.jpg')
def servir_imagem(arquivo):
    nome = arquivo.replace("_", " ")
    partes = nome.split()
    if len(partes) < 4:
        abort(400)  # dados insuficientes

    marca, modelo, cor, ano = partes[0], partes[1], partes[2], partes[3]
    termos = montar_termos(marca, modelo, cor, ano)
    caminho = baixar_e_retornar_caminho(termos)
    if caminho and os.path.exists(caminho):
        return send_file(caminho, mimetype='image/jpeg')
    else:
        abort(404)
