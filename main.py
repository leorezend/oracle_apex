from flask import Flask, send_file, abort, make_response
from baixar_imagem import baixar_e_retornar_caminho
import os

app = Flask(__name__)

@app.route('/imagens/<path:arquivo>.jpg')
def servir_imagem(arquivo):
    nome = arquivo.replace("_", " ")
    caminho = baixar_e_retornar_caminho(nome)

    if caminho and os.path.exists(caminho):
        response = make_response(send_file(caminho, mimetype='image/jpeg'))
        # Força o navegador a NÃO usar cache
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response
    else:
        abort(404)
