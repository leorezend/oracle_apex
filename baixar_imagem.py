import os
import shutil
from icrawler.builtin import GoogleImageCrawler
import cloudinary.uploader
from cloudinary_config import cloudinary

def baixar_e_retornar_url(termos):
    nome_base = termos.replace(" ", "_").lower()
    nome_arquivo = nome_base + ".jpg"
    caminho_arquivo = os.path.join("imagens", nome_arquivo)

    # Verifica se já temos um cache com URL salva
    url_cache_path = caminho_arquivo + ".url"
    if os.path.exists(url_cache_path):
        with open(url_cache_path, "r") as f:
            return f.read()

    # Cria pastas se necessário
    os.makedirs("temp", exist_ok=True)
    os.makedirs("imagens", exist_ok=True)

    # Limpa a pasta temp
    for f in os.listdir("temp"):
        os.remove(os.path.join("temp", f))

    # Busca no Google imagens do carro inteiro (frente ou lateral)
    crawler = GoogleImageCrawler(storage={"root_dir": "temp"})
    crawler.crawl(keyword=termos + " carro inteiro frente ou lateral -logo", max_num=1)

    arquivos = os.listdir("temp")
    if arquivos:
        original = os.path.join("temp", arquivos[0])
        shutil.copy(original, caminho_arquivo)

        # Upload para Cloudinary
        resultado = cloudinary.uploader.upload(
            original,
            public_id=nome_base,
            folder="veiculos_apex",  # opcional, ajuda a organizar
            overwrite=True
        )

        url = resultado["secure_url"]

        # Salva URL em cache para evitar upload repetido
        with open(url_cache_path, "w") as f:
            f.write(url)

        return url

    return None
