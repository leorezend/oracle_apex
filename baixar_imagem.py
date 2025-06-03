import os
from icrawler.builtin import GoogleImageCrawler
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name='dzqt6j9bj',
    api_key='999688376561143',
    api_secret=os.environ.get("CLOUDINARY_SECRET")  # NUNCA fixe no código
)

def montar_termos(marca, modelo, cor, ano):
    termos = f"{marca} {modelo} {ano} {cor} carro inteiro lateral frente -logo -marca -site"
    return termos

def imagem_valida(caminho):
    try:
        with Image.open(caminho) as img:
            largura, altura = img.size
            if largura < 500 or altura < 300 or largura < altura:
                return False
            return True
    except:
        return False

def imagem_ja_no_cloudinary(nome_publico):
    try:
        resultado = cloudinary.api.resource(nome_publico)
        return resultado['secure_url']
    except cloudinary.exceptions.NotFound:
        return None

def baixar_e_retornar_cloudinary_url(termos, tentativas=3):
    nome_publico = termos.replace(" ", "_").lower()
    url_existente = imagem_ja_no_cloudinary(nome_publico)
    if url_existente:
        return url_existente

    os.makedirs("imagens", exist_ok=True)

    for _ in range(tentativas):
        crawler = GoogleImageCrawler(storage={"root_dir": "imagens"})
        crawler.crawl(keyword=termos, max_num=1, file_idx_offset=0)

        arquivos = sorted(
            os.listdir("imagens"),
            key=lambda x: os.path.getctime(os.path.join("imagens", x)),
            reverse=True
        )
        for arq in arquivos:
            if arq.endswith(".jpg"):
                caminho_temp = os.path.join("imagens", arq)
                if imagem_valida(caminho_temp):
                    resultado = cloudinary.uploader.upload(
                        caminho_temp,
                        public_id=nome_publico,
                        folder="veiculos",
                        overwrite=True,
                        resource_type="image"
                    )
                    os.remove(caminho_temp)
                    return resultado['secure_url']
                else:
                    os.remove(caminho_temp)

    return None
