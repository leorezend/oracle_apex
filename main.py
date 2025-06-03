from flask import Flask, request, jsonify
from baixar_imagem import buscar_imagem
import os

app = Flask(__name__)

@app.route("/buscar_imagem", methods=["GET"])
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
