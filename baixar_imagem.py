import os
from icrawler.builtin import GoogleImageCrawler
from PIL import Image

def montar_termos(marca, modelo, cor, ano):
    termos = f"{marca} {modelo} {ano} {cor} carro inteiro lateral frente -logo -marca -site"
    return termos

def imagem_valida(caminho):
    try:
        with Image.open(caminho) as img:
            largura, altura = img.size
            if largura < 500 or altura < 300:
                return False
            if largura < altura:
                return False
            return True
    except:
        return False

def baixar_e_retornar_caminho(termos, tentativas=3):
    nome_arquivo = termos.replace(" ", "_") + ".jpg"
    caminho_arquivo = os.path.join("imagens", nome_arquivo)

    if os.path.exists(caminho_arquivo):
        return caminho_arquivo

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
            if arq.endswith(".jpg") and not arq.startswith(termos.replace(" ", "_")):
                caminho_temp = os.path.join("imagens", arq)
                if imagem_valida(caminho_temp):
                    os.rename(caminho_temp, caminho_arquivo)
                    return caminho_arquivo
                else:
                    os.remove(caminho_temp)

    return None
