from flask import Flask, send_file, abort
from baixar_imagem import baixar_e_retornar_caminho
import os

app = Flask(__name__)

@app.route('/imagens/<path:arquivo>.jpg')
def servir_imagem(arquivo):
    nome = arquivo.replace("_", " ")
    caminho = baixar_e_retornar_caminho(nome)
    if caminho and os.path.exists(caminho):
        return send_file(caminho, mimetype='image/jpeg')
    else:
        abort(404)
