import os
import re
import requests
from PIL import Image
from io import BytesIO
import cloudinary.uploader
import cv2
import numpy as np
from bs4 import BeautifulSoup

cloudinary.config(
    cloud_name="dzqt6j9bj",
    api_key="999688376561143",
    api_secret=os.getenv("CLOUDINARY_SECRET")
)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def sanitize_filename(nome):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", nome)

def tem_rosto(img_pil):
    img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return len(faces) > 0

def proporcao_valida(img_pil):
    w, h = img_pil.size
    ratio = w / h
    return 1.3 < ratio < 1.8 and w >= 400 and h >= 300

def contem_texto(img_pil):
    return False  # Você pode usar pytesseract se quiser OCR real futuramente

def imagem_valida(img_pil):
    return proporcao_valida(img_pil) and not tem_rosto(img_pil) and not contem_texto(img_pil)

def buscar_imagem(marca, modelo, cor, ano):
    termo = f"{marca} {modelo} {ano} {cor} carro de frente ou diagonal"
    url = f"https://www.google.com/search?tbm=isch&q={termo.replace(' ', '+')}"

    resposta = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    imagens = soup.find_all("img")

    for img_tag in imagens[1:15]:
        src = img_tag.get("src")
        if not src or not src.startswith("http"):
            continue

        try:
            imagem_resp = requests.get(src, timeout=5)
            imagem = Image.open(BytesIO(imagem_resp.content)).convert("RGB")

            if imagem_valida(imagem):
                nome = sanitize_filename(f"{marca}_{modelo}_{ano}_{cor}")
                upload_result = cloudinary.uploader.upload(
                    BytesIO(imagem_resp.content),
                    public_id=nome,
                    folder="veiculos_apex",
                    overwrite=True,
                    resource_type="image"
                )
                return upload_result["secure_url"]
        except Exception:
            continue

    return None
