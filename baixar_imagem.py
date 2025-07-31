import os
from icrawler.builtin import GoogleImageCrawler, BingImageCrawler
from PIL import Image
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name='dzqt6j9bj',
    api_key='999688376561143',
    api_secret=os.environ.get("CLOUDINARY_SECRET")
)

def montar_termos(marca, modelo, cor, ano):
    return f"{marca} {modelo} {ano} {cor} carro de frente diagonal em estúdio -site -marca -logo -banner -concessionária -propaganda -placa"

def imagem_valida(caminho):
    try:
        with Image.open(caminho) as img:
            largura, altura = img.size
            if largura < 500 or altura < 300 or largura < altura:
                print(f"[INVALIDA] Dimensões: {largura}x{altura}")
                return False
            return True
    except Exception as e:
        print(f"[ERRO IMG] {e}")
        return False

def imagem_ja_no_cloudinary(nome_publico):
    try:
        resultado = cloudinary.api.resource(nome_publico)
        return resultado['secure_url']
    except cloudinary.exceptions.NotFound:
        return None

def buscar_imagem_com_icrawler(termos, engine="google"):
    crawler_class = GoogleImageCrawler if engine == "google" else BingImageCrawler
    crawler = crawler_class(storage={"root_dir": "imagens"})
    crawler.session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
    })
    crawler.crawl(keyword=termos, max_num=1, file_idx_offset=0)

    arquivos = sorted(
        os.listdir("imagens"),
        key=lambda x: os.path.getctime(os.path.join("imagens", x)),
        reverse=True
    )

    for arq in arquivos:
        caminho_temp = os.path.join("imagens", arq)
        nome_arquivo = arq.lower()
        if any(site in nome_arquivo for site in ['reddit', 'redd', 'pinterest', 'tumblr', 'blogspot']):
            os.remove(caminho_temp)
            continue
        if imagem_valida(caminho_temp):
            return caminho_temp
        os.remove(caminho_temp)

    return None

def baixar_e_retornar_cloudinary_url(termos):
    nome_publico = termos.replace(" ", "_").lower()
    url_existente = imagem_ja_no_cloudinary(nome_publico)
    if url_existente:
        print(f"[CACHE] Imagem existente: {url_existente}")
        return url_existente

    os.makedirs("imagens", exist_ok=True)

    caminho = buscar_imagem_com_icrawler(termos, engine="google")
    if not caminho:
        print("[FALLBACK] Google falhou, tentando Bing...")
        caminho = buscar_imagem_com_icrawler(termos, engine="bing")

    if caminho:
        print(f"[UPLOAD] Subindo imagem válida...")
        resultado = cloudinary.uploader.upload(
            caminho,
            public_id=nome_publico,
            folder="veiculos",
            overwrite=True,
            resource_type="image"
        )
        os.remove(caminho)
        return resultado['secure_url']

    print("[ERRO] Nenhuma imagem válida encontrada.")
    return None
