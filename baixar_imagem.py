import os
import shutil
from icrawler.builtin import GoogleImageCrawler

def baixar_e_retornar_caminho(termos):
    nome_arquivo = termos.replace(" ", "_").lower() + ".jpg"
    caminho_arquivo = os.path.join("imagens", nome_arquivo)

    if os.path.exists(caminho_arquivo):
        return caminho_arquivo

    os.makedirs("temp", exist_ok=True)
    os.makedirs("imagens", exist_ok=True)

    # Limpa a pasta temporária
    for f in os.listdir("temp"):
        os.remove(os.path.join("temp", f))

    crawler = GoogleImageCrawler(storage={"root_dir": "temp"})
    crawler.crawl(keyword=termos + " carro inteiro frente", max_num=1)

    arquivos = os.listdir("temp")
    if arquivos:
        original = os.path.join("temp", arquivos[0])
        shutil.move(original, caminho_arquivo)
        return caminho_arquivo

    return None
