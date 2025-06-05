from flask import Flask, request, jsonify, send_file
from baixar_imagem import buscar_ou_retornar_imagem

app = Flask(__name__)

@app.route("/imagem")
def get_imagem():
    marca = request.args.get("marca")
    modelo = request.args.get("modelo")
    cor = request.args.get("cor")
    ano = request.args.get("ano")

    if not all([marca, modelo, cor, ano]):
        return jsonify({"erro": "Parâmetros obrigatórios: marca, modelo, cor, ano"}), 400

    caminho = buscar_ou_retornar_imagem(marca, modelo, cor, ano)
    if caminho:
        return send_file(caminho, mimetype='image/jpeg')
    else:
        return jsonify({"erro": "Imagem não encontrada"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
