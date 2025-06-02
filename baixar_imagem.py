import os
from icrawler.builtin import GoogleImageCrawler
from urllib.parse import quote

def baixar_e_retornar_caminho(termos):
    nome_arquivo = termos.replace(" ", "_") + ".jpg"
    caminho_arquivo = os.path.join("imagens", nome_arquivo)

    if os.path.exists(caminho_arquivo):
        return caminho_arquivo

    os.makedirs("imagens", exist_ok=True)

    crawler = GoogleImageCrawler(storage={"root_dir": "imagens"})
    crawler.crawl(keyword=termos + " carro inteiro frente", max_num=1, file_idx_offset=0)

    arquivos = os.listdir("imagens")
    for arq in arquivos:
        if arq.endswith(".jpg") and not arq.startswith(nome_arquivo):
            os.rename(os.path.join("imagens", arq), caminho_arquivo)
            return caminho_arquivo

    return None