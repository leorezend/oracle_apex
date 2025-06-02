from flask import Flask, redirect, abort
from baixar_imagem import baixar_e_retornar_url

app = Flask(__name__)

@app.route('/imagens/<path:arquivo>.jpg')
def servir_imagem(arquivo):
    nome = arquivo.replace("_", " ")
    url = baixar_e_retornar_url(nome)

    if url:
        return redirect(url)
    else:
        abort(404)
