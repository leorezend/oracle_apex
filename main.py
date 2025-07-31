from flask import Flask, redirect, abort
from baixar_imagem import montar_termos, baixar_e_retornar_cloudinary_url

app = Flask(__name__)

@app.route('/imagens/<path:arquivo>.jpg')
def servir_imagem(arquivo):
    nome = arquivo.replace("_", " ")
    partes = nome.split()
    if len(partes) < 4:
        abort(400)

    marca, modelo, cor, ano = partes[0], partes[1], partes[2], partes[3]
    termos = montar_termos(marca, modelo, cor, ano)
    url = baixar_e_retornar_cloudinary_url(termos)

    if url:
        url_otimizada = url.replace("upload/", "upload/f_auto,q_auto/")
        return redirect(url_otimizada)
    else:
        abort(404)
