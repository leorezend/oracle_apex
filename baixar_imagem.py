import os
import hashlib
import tempfile
import requests
from urllib.parse import quote
from PIL import Image
import cloudinary.uploader
import cloudinary.api
from colorthief import ColorThief

cloudinary.config(
    cloud_name="dzqt6j9bj",
    api_key="999688376561143",
    api_secret=os.getenv("CLOUDINARY_SECRET")
)

def gerar_nome_imagem(marca, modelo, cor, ano):
    chave = f"{marca}_{modelo}_{cor}_{ano}".lower().replace(" ", "_")
    return hashlib.md5(chave.encode()).hexdigest()

def buscar_ou_retornar_imagem(marca, modelo, cor, ano):
    nome_imagem = gerar_nome_imagem(marca, modelo, cor, ano)
    public_id = f"veiculos/{nome_imagem}"

    try:
        url = cloudinary.api.resource(public_id)["secure_url"]
        resposta = requests.get(url, stream=True)
        if resposta.status_code == 200:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
                for chunk in resposta.iter_content(1024):
                    temp_file.write(chunk)
                return temp_file.name
    except:
        pass

    urls = buscar_imagens_no_google(marca, modelo, ano)
    for url in urls:
        try:
            img_temp = baixar_imagem_temp(url)
            if not img_temp:
                continue

            if not cor_dominante_bate(img_temp, cor):
                continue

            upload = cloudinary.uploader.upload(img_temp, public_id=public_id, overwrite=True)
            return img_temp
        except:
            continue
    return None

def buscar_imagens_no_google(marca, modelo, ano):
    query = quote(f"{marca} {modelo} {ano} carro")
    endpoint = f"https://www.googleapis.com/customsearch/v1?q={query}&searchType=image&key=SUA_API&cx=SEU_CX"
    resp = requests.get(endpoint)
    if resp.status_code != 200:
        return []
    data = resp.json()
    return [item["link"] for item in data.get("items", [])]

def baixar_imagem_temp(url):
    try:
        resposta = requests.get(url, timeout=5)
        if resposta.status_code != 200:
            return None
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
            temp_file.write(resposta.content)
            return temp_file.name
    except:
        return None

def cor_dominante_bate(caminho, cor_esperada):
    try:
        dominante = ColorThief(caminho).get_color(quality=1)
        cor_esperada = cor_esperada.lower()
        branco = (200, 200, 200)
        preto = (50, 50, 50)

        if cor_esperada == "preta":
            return all(c <= 80 for c in dominante)
        elif cor_esperada == "branca":
            return all(c >= 200 for c in dominante)
        else:
            return True  # Aceita qualquer outra cor por enquanto
    except:
        return True